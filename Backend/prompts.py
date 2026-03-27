"""
Prompt templates for all agents.
Each prompt is a (system, user) tuple factory function.
"""

# ══════════════════════════════════════════════════════════════════════════════
# KEYWORD CLUSTERING PROMPTS
# ══════════════════════════════════════════════════════════════════════════════

def keyword_cluster_prompts(seed_keyword: str, location: str, cluster_count: int) -> tuple[str, str]:
    system = """You are a senior SEO strategist specializing in keyword research.
You cluster keywords by search intent and estimate realistic traffic potential.
You MUST return valid, well-formatted JSON only — no markdown, no explanation."""

    user = f"""Analyze the seed keyword: "{seed_keyword}" for the target location: "{location}".

Generate exactly {cluster_count} keyword clusters. For each cluster, provide:
- cluster_name: short descriptive name (string)
- intent: one of [informational, transactional, navigational, commercial] (string)
- keywords: list of 4-6 related keywords (array of strings)
- estimated_monthly_searches: realistic range string e.g. "1,000-5,000" (string)
- difficulty: one of [low, medium, high] (string)
- priority_score: priority score 0-10 (number)

Also provide:
- recommended_primary: the single best keyword to target first (string)
- traffic_potential: overall traffic opportunity description (string)

Return ONLY valid JSON with this exact structure:
{{
  "seed_keyword": "{seed_keyword}",
  "clusters": [
    {{
      "cluster_name": "Example Cluster",
      "intent": "informational",
      "keywords": ["keyword1", "keyword2", "keyword3"],
      "estimated_monthly_searches": "5,000-10,000",
      "difficulty": "medium",
      "priority_score": 7.5
    }}
  ],
  "total_keywords": <total count as number>,
  "recommended_primary": "{seed_keyword}",
  "traffic_potential": "High opportunity with moderate competition"
}}"""
    return system, user


# ══════════════════════════════════════════════════════════════════════════════
# SERP GAP ANALYSIS PROMPTS
# ══════════════════════════════════════════════════════════════════════════════

def serp_gap_prompts(keyword: str, serp_data: list[dict], page_texts: list[str]) -> tuple[str, str]:
    system = """You are an expert content strategist and SERP analyst.
Given the top search results for a keyword, identify:
1. The dominant SERP personality (listicle, long-form, guide, etc.)
2. Content gaps that top results ALL missed
3. The best angle to outrank them
Return valid JSON only."""

    serp_summary = "\n".join(
        [f"Rank {i+1}: {r['title']} — {r['snippet'][:150]}" for i, r in enumerate(serp_data[:8])]
    )

    # Summarize page texts (first 300 words each)
    page_summary = "\n---\n".join(
        [f"Page {i+1} content preview: {' '.join(t.split()[:200])}" for i, t in enumerate(page_texts[:5]) if t]
    )

    user = f"""Keyword: "{keyword}"

TOP SERP RESULTS:
{serp_summary}

COMPETITOR CONTENT PREVIEWS:
{page_summary}

Analyze and return this exact JSON:
{{
  "serp_personality": "<dominant format>",
  "content_gaps": [
    {{"topic": "<gap>", "importance": "high|medium|low", "reason": "<why it matters>"}}
  ],
  "recommended_format": "<best format to use>",
  "recommended_word_count": <int>,
  "winning_angle": "<unique angle to outrank all competitors>"
}}"""
    return system, user


# ══════════════════════════════════════════════════════════════════════════════
# BLOG GENERATION PROMPTS
# ══════════════════════════════════════════════════════════════════════════════

def blog_generation_prompts(
    keyword: str,
    secondary_keywords: list[str],
    location: str,
    word_count: int,
    tone: str,
    content_gaps: list[str],
    serp_personality: str,
    winning_angle: str,
    competitor_gaps: list[str],
    internal_links: list[dict],
    title: str | None,
) -> tuple[str, str]:

    secondary_str = ", ".join(secondary_keywords) if secondary_keywords else "none"
    gaps_str = "\n".join([f"- {g}" for g in content_gaps]) if content_gaps else "- Use your expertise"
    il_str = (
        "\n".join([f"- [{l['title']}]({l['url']})" for l in internal_links])
        if internal_links else "None provided"
    )
    title_instruction = (
        f'Use this exact title: "{title}"' if title
        else f'Create an SEO-optimized title containing "{keyword}"'
    )

    system = f"""You are a world-class SEO content writer specializing in the Indian market.
You write {word_count}-word blogs that rank on Google and win featured snippets.
Your writing is {tone}, deeply informative, and human-sounding.
You NEVER use phrases like "In conclusion", "It is worth noting", "Delve into", or "In today's world".
You vary sentence lengths naturally — short punchy sentences mixed with longer explanatory ones.
Always use proper markdown: # for H1, ## for H2, ### for H3, **bold**, bullet lists."""

    user = f"""Write a complete, publish-ready blog post.

PRIMARY KEYWORD: {keyword}
SECONDARY KEYWORDS: {secondary_str}
TARGET LOCATION: {location}
FORMAT STYLE: {serp_personality}
WINNING ANGLE: {winning_angle}
WORD COUNT TARGET: {word_count} words
TITLE: {title_instruction}

MANDATORY CONTENT GAPS TO COVER (competitors missed these):
{gaps_str}

INTERNAL LINKS TO WEAVE IN NATURALLY:
{il_str}

STRUCTURE REQUIREMENTS:
1. H1 title containing primary keyword
2. Meta description (150-160 chars) in a blockquote at the top labeled "META:"
3. Strong intro (first 100 words MUST contain "{keyword}")
4. At least 6 H2 sections
5. At least 2 H3 subsections
6. One 40-60 word paragraph specifically optimized as a featured snippet answer (label with HTML comment <!-- SNIPPET -->)
7. One numbered list and one bullet list
8. One comparison table if relevant
9. CTA section at the end
10. Use secondary keywords naturally throughout

Write the complete blog now:"""

    return system, user


# ══════════════════════════════════════════════════════════════════════════════
# HUMANIZATION PROMPTS
# ══════════════════════════════════════════════════════════════════════════════

def humanization_prompts(content: str, ai_flags: list[str]) -> tuple[str, str]:
    flags_str = "\n".join(ai_flags) if ai_flags else "General AI patterns detected"

    system = """You are an expert human editor who rewrites AI-generated blog content to sound authentically human.
Rules:
- Vary sentence lengths drastically (3-word sentences next to 25-word ones)
- Add first-person observations, opinions, rhetorical questions
- Replace AI clichés with specific, concrete language
- Add Indian-market specific examples and references
- Keep all SEO structure, headings, keywords, and links INTACT
- Do NOT change the meaning or remove any information
- Return the full rewritten blog in markdown"""

    user = f"""Rewrite this blog to sound more human. These AI patterns were detected:
{flags_str}

ORIGINAL BLOG:
{content}

Rewrite the COMPLETE blog, preserving all structure and keywords:"""

    return system, user


# ══════════════════════════════════════════════════════════════════════════════
# SNIPPET OPTIMIZATION PROMPTS
# ══════════════════════════════════════════════════════════════════════════════

def snippet_optimization_prompts(keyword: str, context: str) -> tuple[str, str]:
    system = """You are a featured snippet optimization expert.
You create 3 variants of a featured snippet answer: paragraph, numbered list, and table.
Return valid JSON only."""

    user = f"""Keyword: "{keyword}"

Context from blog:
{context[:1500]}

Create 3 featured snippet variants optimized for Google's featured snippet box.
Return this JSON:
{{
  "paragraph_variant": "<40-60 word direct answer>",
  "list_variant": "<numbered list with 4-6 items as a string>",
  "table_variant": "<markdown table if applicable, else null>",
  "readiness_probability": <float 0-100>,
  "optimization_tips": ["tip1", "tip2", "tip3"]
}}"""

    return system, user


# ══════════════════════════════════════════════════════════════════════════════
# INTERNAL LINKING PROMPTS
# ══════════════════════════════════════════════════════════════════════════════

def internal_linking_prompts(content: str, existing_blogs: list[dict], primary_keyword: str) -> tuple[str, str]:
    blogs_str = "\n".join(
        [f"- Title: {b['title']} | URL: {b['url']} | Topic: {b.get('topic','')} | Keywords: {', '.join(b.get('keywords',[]))}"
         for b in existing_blogs]
    )

    system = """You are an internal linking strategist for an SEO blog platform.
You identify the best anchor texts and placements to link related blog posts.
Return valid JSON only."""

    user = f"""Primary blog keyword: "{primary_keyword}"

EXISTING BLOG POSTS TO LINK FROM:
{blogs_str}

BLOG CONTENT (first 2000 chars):
{content[:2000]}

Suggest internal link placements. Return this JSON:
{{
  "suggestions": [
    {{
      "anchor_text": "<exact text to hyperlink>",
      "target_url": "<url from above list>",
      "target_title": "<blog title>",
      "relevance_score": <float 0-10>,
      "placement_hint": "<sentence or paragraph context where this link fits>",
      "reason": "<why this link adds value>"
    }}
  ],
  "linking_score": <float 0-100>
}}"""

    return system, user


# ══════════════════════════════════════════════════════════════════════════════
# TITLE & META GENERATION
# ══════════════════════════════════════════════════════════════════════════════

def title_meta_prompts(keyword: str, content_summary: str, location: str) -> tuple[str, str]:
    system = """You are an SEO title and meta description expert.
Return valid JSON only."""

    user = f"""Keyword: "{keyword}" | Location: "{location}"
Content summary: {content_summary[:500]}

Generate:
- title: SEO-optimized H1 (50-60 chars, includes keyword)
- meta_description: 150-160 chars, includes keyword, has CTA
- slug: URL-friendly slug

Return JSON: {{"title": "", "meta_description": "", "slug": ""}}"""

    return system, user
