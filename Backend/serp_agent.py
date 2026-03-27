"""
Agent 2 — SERP Gap Analysis Agent
────────────────────────────────────
1. Scrapes DuckDuckGo for top results
2. Fetches competitor page text concurrently
3. Sends everything to Groq for gap analysis
"""

import asyncio
from scraper import get_serp_results, fetch_multiple_pages
from groq_service import chat_completion_json
from prompts import serp_gap_prompts
from response_models import SERPResult, SERPGap, SERPAnalysisResponse
from config import MAX_SERP_RESULTS


def _detect_content_type(title: str, snippet: str) -> str:
    combined = (title + " " + snippet).lower()
    if any(w in combined for w in ["best", "top", "list", "ways", "tips"]):
        return "listicle"
    if any(w in combined for w in ["how to", "guide", "tutorial", "step"]):
        return "guide"
    if any(w in combined for w in ["vs", "versus", "compare", "comparison"]):
        return "comparison"
    if "?" in title:
        return "qa"
    return "long-form"


async def run_serp_analysis(
    keyword: str,
    target_location: str = "India",
    max_results: int = MAX_SERP_RESULTS,
    competitor_urls: list[str] | None = None,
) -> SERPAnalysisResponse:
    """
    Entry point for the SERP Gap Analysis Agent.
    """
    # Step 1: Fetch SERP results
    raw_results = await get_serp_results(keyword, max_results)

    # Step 2: Build SERPResult objects
    serp_results = []
    for i, r in enumerate(raw_results):
        serp_results.append(
            SERPResult(
                rank=i + 1,
                title=r["title"],
                url=r["url"],
                snippet=r["snippet"],
                word_count_estimate=0,          # will fill after fetch
                has_featured_snippet=(i == 0),  # first result often has snippet
                content_type=_detect_content_type(r["title"], r["snippet"]),
            )
        )

    # Step 3: Fetch competitor pages (top 5 + any provided URLs)
    urls_to_fetch = [r.url for r in serp_results[:5]]
    if competitor_urls:
        urls_to_fetch = list(set(urls_to_fetch + competitor_urls))[:8]

    page_texts = await fetch_multiple_pages(urls_to_fetch)

    # Update word counts
    for i, text in enumerate(page_texts):
        if i < len(serp_results):
            serp_results[i].word_count_estimate = len(text.split()) if text else 500

    avg_word_count = (
        sum(r.word_count_estimate for r in serp_results if r.word_count_estimate) //
        max(1, sum(1 for r in serp_results if r.word_count_estimate))
    )

    # Step 4: LLM gap analysis
    raw_data = [{"title": r.title, "snippet": r.snippet, "url": r.url} for r in serp_results]
    system, user = serp_gap_prompts(keyword, raw_data, page_texts)
    llm_data = await chat_completion_json(system, user, temperature=0.3)

    gaps = [
        SERPGap(
            topic=g.get("topic", ""),
            importance=g.get("importance", "medium"),
            reason=g.get("reason", ""),
        )
        for g in llm_data.get("content_gaps", [])
    ]

    return SERPAnalysisResponse(
        keyword=keyword,
        serp_personality=llm_data.get("serp_personality", "long-form"),
        results=serp_results,
        content_gaps=gaps,
        average_word_count=avg_word_count or 1200,
        recommended_format=llm_data.get("recommended_format", "long-form guide"),
        recommended_word_count=llm_data.get("recommended_word_count", 2500),
        winning_angle=llm_data.get("winning_angle", "Comprehensive India-specific guide"),
    )
