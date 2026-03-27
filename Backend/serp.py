"""
POST /serp/analyze — Standalone SERP gap analysis endpoint.
"""

from fastapi import APIRouter, HTTPException
from request_models import SERPAnalysisRequest
from response_models import SERPAnalysisResponse
from serp_agent import run_serp_analysis

router = APIRouter(prefix="/serp", tags=["SERP Analysis"])


@router.post("/analyze", response_model=SERPAnalysisResponse)
async def analyze_serp(req: SERPAnalysisRequest):
    """
    Scrapes top SERP results for a keyword, fetches competitor
    page content, and identifies content gaps using Groq LLM.

    Returns:
    - SERP personality (dominant content format)
    - Content gaps competitors missed
    - Recommended format + word count
    - Winning angle to outrank all results
    """
    try:
        return await run_serp_analysis(
            keyword=req.keyword,
            target_location=req.target_location,
            max_results=req.max_results,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SERP analysis failed: {str(e)}")
