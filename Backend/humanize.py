"""
POST /humanize — Standalone humanization endpoint.
Takes any blog content, runs AI detection, then rewrites if needed.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, model_validator
from humanizer import run_humanization
from ai_detection_service import analyze_ai_probability
from response_models import AIDetectionResponse

router = APIRouter(prefix="/humanize", tags=["Humanization"])


class HumanizeRequest(BaseModel):
    content: str = Field(..., min_length=1)
    force: bool = Field(default=False, description="Force humanization even if score is already low")

    @model_validator(mode="before")
    @classmethod
    def normalize_payload(cls, values):
        """Accept common payload keys from clients that don't use `content`."""
        if not isinstance(values, dict):
            return values

        content = values.get("content")
        if not content:
            content = values.get("text") or values.get("blog_content")
            if content:
                values["content"] = content
        return values


class HumanizeResponse(BaseModel):
    original_ai_probability: float
    final_ai_probability: float
    naturalness_improvement: float
    content: str
    was_humanized: bool
    before_detection: AIDetectionResponse
    after_detection: AIDetectionResponse


@router.post("/", response_model=HumanizeResponse)
async def humanize_content(req: HumanizeRequest):
    """
    Analyze + optionally rewrite blog content to reduce AI detection score.

    Flow:
    1. Run AI detection on original content
    2. If ai_probability > 45% (or force=True), rewrite with humanization agent
    3. Re-score after rewriting
    4. Return both versions + improvement delta
    """
    try:
        if len(req.content.strip()) < 100:
            raise HTTPException(
                status_code=400,
                detail="content must be at least 100 characters for reliable AI detection/humanization",
            )

        # Step 1: Detect AI on original
        before_dict = analyze_ai_probability(req.content)
        original_prob = before_dict["ai_probability_percent"]

        # Step 2+3: Humanize and re-detect
        humanized_content, after_dict = await run_humanization(
            content=req.content,
            ai_detection_result=before_dict,
            force=req.force,
        )

        was_humanized = humanized_content != req.content
        final_prob = after_dict["ai_probability_percent"]
        improvement = round(original_prob - final_prob, 1)

        return HumanizeResponse(
            original_ai_probability=original_prob,
            final_ai_probability=final_prob,
            naturalness_improvement=improvement,
            content=humanized_content,
            was_humanized=was_humanized,
            before_detection=AIDetectionResponse(**before_dict),
            after_detection=AIDetectionResponse(**after_dict),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Humanization failed: {str(e)}")
