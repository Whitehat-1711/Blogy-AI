"""
Agent 3 — Blog Generation Agent
─────────────────────────────────
Generates a full SEO blog using Groq LLM, guided by SERP analysis
and keyword cluster data.
"""

import re
from groq_service import chat_completion, chat_completion_json
from prompts import blog_generation_prompts, title_meta_prompts
from response_models import SERPAnalysisResponse, KeywordClusterResponse
from slugify import slugify


async def run_blog_generation(
    keyword: str,
    secondary_keywords: list[str],
    target_location: str,
    word_count: int,
    tone: str,
    serp_analysis: SERPAnalysisResponse | None,
    keyword_clusters: KeywordClusterResponse | None,
    internal_links: list[dict],
    title_override: str | None,
) -> dict:
    """
    Generates the blog post and returns a dict with:
    { title, meta_description, slug, content }
    """
    # Extract SERP intelligence
    content_gaps: list[str] = []
    serp_personality = "long-form guide"
    winning_angle = "Comprehensive, India-specific expert guide"

    if serp_analysis:
        content_gaps = [g.topic for g in serp_analysis.content_gaps]
        serp_personality = serp_analysis.serp_personality
        winning_angle = serp_analysis.winning_angle
        if word_count < serp_analysis.recommended_word_count:
            word_count = serp_analysis.recommended_word_count

    # Generate the blog
    system, user = blog_generation_prompts(
        keyword=keyword,
        secondary_keywords=secondary_keywords,
        location=target_location,
        word_count=word_count,
        tone=tone,
        content_gaps=content_gaps,
        serp_personality=serp_personality,
        winning_angle=winning_angle,
        competitor_gaps=content_gaps,
        internal_links=internal_links,
        title=title_override,
    )

    content = await chat_completion(system, user, temperature=0.75, max_tokens=8000)

    # Extract meta description if embedded in content
    meta_description = ""
    meta_match = re.search(r"META:\s*(.+?)(?:\n|$)", content, re.IGNORECASE)
    if meta_match:
        meta_description = meta_match.group(1).strip().strip('"')

    # Extract H1 title from content
    title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    extracted_title = title_match.group(1).strip() if title_match else keyword

    # If no meta in content, generate separately
    if not meta_description:
        t_system, t_user = title_meta_prompts(
            keyword, extracted_title, target_location
        )
        try:
            meta_data = await chat_completion_json(t_system, t_user, temperature=0.3)
            meta_description = meta_data.get("meta_description", "")
        except Exception:
            meta_description = f"Discover everything about {keyword} in India. Expert guide covering tips, strategies, and tools."

    title = title_override or extracted_title
    slug = slugify(title)

    return {
        "title": title,
        "meta_description": meta_description[:160],
        "slug": slug,
        "content": content,
    }
