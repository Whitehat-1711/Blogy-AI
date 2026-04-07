"""
Unified LLM service with provider routing:
- Groq primary for long-form generation tasks
- Gemini fallback/auxiliary routing for lower-cost analysis tasks
"""

import json
import re
import logging
import asyncio
import time
from groq import AsyncGroq
import google.generativeai as genai

# Handle imports with fallback for different module contexts
try:
    from Backend.core.config import (
        GROQ_API_KEY,
        GROQ_MODEL,
        GROQ_MAX_TOKENS,
        GROQ_TEMPERATURE,
        GROQ_MAX_RETRIES,
        GROQ_MAX_CONCURRENCY,
        GEMINI_API_KEY,
        GEMINI_ENABLED,
        GEMINI_MODEL_FAST,
        LLM_PRIMARY_PROVIDER,
        LLM_FALLBACK_PROVIDER,
    )
except ImportError:
    from ..core.config import (
        GROQ_API_KEY,
        GROQ_MODEL,
        GROQ_MAX_TOKENS,
        GROQ_TEMPERATURE,
        GROQ_MAX_RETRIES,
        GROQ_MAX_CONCURRENCY,
        GEMINI_API_KEY,
        GEMINI_ENABLED,
        GEMINI_MODEL_FAST,
        LLM_PRIMARY_PROVIDER,
        LLM_FALLBACK_PROVIDER,
    )

logger = logging.getLogger("blogy")

_client: AsyncGroq | None = None
_request_semaphore = asyncio.Semaphore(max(1, GROQ_MAX_CONCURRENCY))
_gemini_semaphore = asyncio.Semaphore(max(1, GROQ_MAX_CONCURRENCY))
_gemini_model_cache: str | None = None
_gemini_disabled_runtime = False
_gemini_retry_after_ts = 0.0

_GROQ_HEAVY_TASKS = {"blog_generation", "content_expansion", "humanization"}
_AUX_TASKS = {"keyword_cluster", "serp_analysis", "web_insights", "snippet", "internal_linking", "meta"}


def get_client() -> AsyncGroq:
    global _client
    if _client is None:
        _client = AsyncGroq(api_key=GROQ_API_KEY, max_retries=max(0, GROQ_MAX_RETRIES))
    return _client


def _gemini_available() -> bool:
    if _gemini_retry_after_ts and time.time() < _gemini_retry_after_ts:
        return False
    return bool(GEMINI_ENABLED and GEMINI_API_KEY and not _gemini_disabled_runtime)


def _extract_retry_seconds(error_message: str) -> int:
    match = re.search(r"retry in\s+(\d+(?:\.\d+)?)s", error_message, re.IGNORECASE)
    if not match:
        return 60
    try:
        return max(5, int(float(match.group(1))))
    except ValueError:
        return 60


def _normalize_model_name(name: str) -> str:
    return name.split("/", 1)[-1].strip()


def _resolve_gemini_model() -> str:
    global _gemini_model_cache
    if _gemini_model_cache:
        return _gemini_model_cache

    requested = _normalize_model_name(GEMINI_MODEL_FAST)
    candidates = [requested, "gemini-2.0-flash", "gemini-1.5-flash-latest", "gemini-1.5-flash"]
    candidates = list(dict.fromkeys(candidates))
    fallback = candidates[0]

    try:
        models = list(genai.list_models())
        valid = {
            _normalize_model_name(m.name)
            for m in models
            if "generateContent" in getattr(m, "supported_generation_methods", [])
        }
        for c in candidates:
            if c in valid:
                _gemini_model_cache = c
                return c
    except Exception as e:
        logger.warning(f"Could not list Gemini models, using configured fallback: {e}")

    _gemini_model_cache = fallback
    return fallback


def _preferred_provider(task: str) -> str:
    task = (task or "default").lower()
    primary = (LLM_PRIMARY_PROVIDER or "groq").lower()
    fallback = (LLM_FALLBACK_PROVIDER or "gemini").lower()

    if task in _GROQ_HEAVY_TASKS:
        return "groq"
    if task in _AUX_TASKS and _gemini_available():
        return "gemini"
    if primary == "gemini" and _gemini_available():
        return "gemini"
    if primary == "groq":
        return "groq"
    return fallback if fallback in {"groq", "gemini"} else "groq"


async def _chat_completion_groq(
    system_prompt: str,
    user_prompt: str,
    temperature: float,
    max_tokens: int,
    json_mode: bool,
) -> str:
    client = get_client()
    kwargs: dict = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}
    async with _request_semaphore:
        response = await client.chat.completions.create(**kwargs)
    return response.choices[0].message.content or ""


async def _chat_completion_gemini(
    system_prompt: str,
    user_prompt: str,
    temperature: float,
    max_tokens: int,
    json_mode: bool,
) -> str:
    global _gemini_disabled_runtime, _gemini_model_cache, _gemini_retry_after_ts
    genai.configure(api_key=GEMINI_API_KEY)
    model_name = _resolve_gemini_model()
    model = genai.GenerativeModel(model_name)
    prompt = f"{system_prompt}\n\n{user_prompt}"
    if json_mode:
        prompt += "\n\nReturn ONLY valid JSON. No markdown fences."
    generation_config = genai.types.GenerationConfig(
        temperature=temperature,
        max_output_tokens=max_tokens,
    )
    try:
        async with _gemini_semaphore:
            response = await model.generate_content_async(
                prompt,
                generation_config=generation_config,
            )
        return (response.text or "").strip()
    except Exception as e:
        message = str(e)
        if "is not found" in message or "not supported for generateContent" in message:
            # Disable Gemini for the process after model resolution failures to avoid repeated slow fallbacks.
            _gemini_disabled_runtime = True
            _gemini_model_cache = None
            logger.warning("Disabling Gemini at runtime due to invalid/unsupported model configuration.")
        elif "Quota exceeded" in message or "RESOURCE_EXHAUSTED" in message:
            retry_seconds = _extract_retry_seconds(message)
            _gemini_retry_after_ts = time.time() + retry_seconds
            logger.warning(f"Gemini quota exhausted. Cooling down Gemini routing for {retry_seconds}s.")
        raise


async def chat_completion(
    system_prompt: str,
    user_prompt: str,
    temperature: float = GROQ_TEMPERATURE,
    max_tokens: int = GROQ_MAX_TOKENS,
    json_mode: bool = False,
    task: str = "default",
) -> str:
    """
    Single call to Groq. Returns raw string content.
    Set json_mode=True to force JSON output (sets response_format).
    """
    provider = _preferred_provider(task)
    try:
        if provider == "gemini" and _gemini_available():
            content = await _chat_completion_gemini(
                system_prompt, user_prompt, temperature, max_tokens, json_mode
            )
        else:
            content = await _chat_completion_groq(
                system_prompt, user_prompt, temperature, max_tokens, json_mode
            )
        logger.debug(f"LLM call successful ({provider}), response length: {len(content)}")
        return content
    except Exception as e:
        # Automatic provider fallback keeps pipeline alive under rate limits.
        fallback = "groq" if provider == "gemini" else "gemini"
        if fallback == "gemini" and not _gemini_available():
            logger.error(f"LLM API error ({provider}): {str(e)}", exc_info=True)
            raise
        try:
            logger.warning(f"Provider {provider} failed for task '{task}', trying {fallback}: {e}")
            if fallback == "gemini":
                return await _chat_completion_gemini(
                    system_prompt, user_prompt, temperature, max_tokens, json_mode
                )
            return await _chat_completion_groq(
                system_prompt, user_prompt, temperature, max_tokens, json_mode
            )
        except Exception:
            logger.error(f"LLM API error with both providers for task '{task}'", exc_info=True)
            raise


async def chat_completion_json(
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.3,
    max_tokens: int = GROQ_MAX_TOKENS,
    task: str = "default",
) -> dict:
    """
    Wrapper that guarantees a parsed dict back.
    Falls back to regex extraction if Groq's JSON mode fails.
    """
    try:
        raw = await chat_completion(
            system_prompt, user_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            json_mode=True,
            task=task,
        )
        logger.debug(f"Groq response (first 500 chars): {raw[:500]}")
        return json.loads(raw)
    except json.JSONDecodeError as e:
        logger.warning(f"JSON decode error, attempting regex extraction: {e}")
        # Attempt to extract the first JSON object from the raw string
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError as e2:
                logger.error(f"Failed to parse extracted JSON: {e2}")
                logger.error(f"Raw response: {raw}")
                raise ValueError(f"Could not parse JSON from Groq response:\n{raw[:500]}")
        logger.error(f"No JSON found in response: {raw}")
        raise ValueError(f"Could not parse JSON from Groq response:\n{raw[:500]}")
