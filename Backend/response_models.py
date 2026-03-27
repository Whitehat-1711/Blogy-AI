from pydantic import BaseModel, Field
from typing import Optional, Any


# ── Keyword Clustering ────────────────────────────────────────────────────────
class KeywordCluster(BaseModel):
    cluster_name: str
    intent: str                    # informational | transactional | navigational | commercial
    keywords: list[str]
    estimated_monthly_searches: str
    difficulty: str                # low | medium | high
    priority_score: float


class KeywordClusterResponse(BaseModel):
    seed_keyword: str
    clusters: list[KeywordCluster]
    total_keywords: int
    recommended_primary: str
    traffic_potential: str


# ── SERP Gap ──────────────────────────────────────────────────────────────────
class SERPResult(BaseModel):
    rank: int
    title: str
    url: str
    snippet: str
    word_count_estimate: int
    has_featured_snippet: bool
    content_type: str              # listicle | long-form | guide | comparison | qa


class SERPGap(BaseModel):
    topic: str
    importance: str                # high | medium | low
    reason: str


class SERPAnalysisResponse(BaseModel):
    keyword: str
    serp_personality: str          # dominant content format on this SERP
    results: list[SERPResult]
    content_gaps: list[SERPGap]
    average_word_count: int
    recommended_format: str
    recommended_word_count: int
    winning_angle: str


# ── SEO Metrics ───────────────────────────────────────────────────────────────
class KeywordDensityDetail(BaseModel):
    keyword: str
    count: int
    density_percent: float
    status: str                    # optimal | under | over


class SEOScoreResponse(BaseModel):
    overall_score: float           # 0-100
    keyword_density: list[KeywordDensityDetail]
    readability_score: float       # Flesch-Kincaid 0-100
    readability_grade: str
    word_count: int
    heading_count: int
    has_meta_structure: bool
    internal_link_count: int
    keyword_in_title: bool
    keyword_in_first_100_words: bool
    lsi_keywords_found: list[str]
    issues: list[str]
    recommendations: list[str]
    projected_traffic_potential: str


# ── AI Detection ──────────────────────────────────────────────────────────────
class AIDetectionResponse(BaseModel):
    ai_probability_percent: float
    naturalness_score: float       # 0-100 (higher = more human)
    burstiness_score: float        # sentence length variance
    perplexity_indicator: str      # low | medium | high
    flags: list[str]               # specific patterns that triggered detection
    verdict: str                   # likely_ai | borderline | likely_human


# ── Snippet ───────────────────────────────────────────────────────────────────
class SnippetVariant(BaseModel):
    type: str                      # paragraph | list | table
    content: str
    word_count: int
    snippet_score: float


class SnippetOptimizationResponse(BaseModel):
    keyword: str
    readiness_probability: float   # 0-100
    recommended_variant: SnippetVariant
    all_variants: list[SnippetVariant]
    optimization_tips: list[str]


# ── Internal Links ────────────────────────────────────────────────────────────
class InternalLinkSuggestion(BaseModel):
    anchor_text: str
    target_url: str
    target_title: str
    relevance_score: float
    placement_hint: str            # paragraph / sentence context hint
    reason: str


class InternalLinkResponse(BaseModel):
    total_suggestions: int
    suggestions: list[InternalLinkSuggestion]
    linking_score: float           # 0-100


# ── Blog Generation ───────────────────────────────────────────────────────────
class BlogGenerationResponse(BaseModel):
    title: str
    meta_description: str
    slug: str
    content: str
    word_count: int

    # All metric scores
    seo_score: SEOScoreResponse
    ai_detection: AIDetectionResponse
    snippet_optimization: SnippetOptimizationResponse
    internal_links: InternalLinkResponse
    keyword_clusters: Optional[KeywordClusterResponse] = None
    serp_analysis: Optional[SERPAnalysisResponse] = None

    generation_time_seconds: float
    model_used: str
