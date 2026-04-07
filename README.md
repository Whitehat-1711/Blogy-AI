# 🚀 Blogy — AI-Powered SEO Blog Generation Engine

> **Production-grade multi-agent SEO blog engine** powered by Groq's `llama-3.3-70b-versatile` LLM.
> Generates SEO-optimized, content-gap-aware blogs with real-time web search, comprehensive competitor analysis, and AI humanization.
> Built for Bizmark'26 — Prompt & Profit hackathon.

---

## Table of Contents

- [System Architecture](#system-architecture)
- [Technology Stack](#technology-stack)
- [8-Step Blog Generation Pipeline](#8-step-blog-generation-pipeline)
- [API Endpoints & Specifications](#api-endpoints--specifications)
- [Data Models](#data-models)
- [Database Schema](#database-schema)
- [Feature Specifications](#feature-specifications)
- [Setup & Deployment](#setup--deployment)
- [Performance & Optimization](#performance--optimization)

---

## System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       FRONTEND (React + Vite)                               │
│  ┌──────────────┐  ┌─────────────┐  ┌────────────┐  ┌──────────────────┐  │
│  │ BlogGenPage  │  │ JournalPage │  │SerpPage   │  │SEOAuditPage     │  │
│  │ (Main UI)    │  │(Blog History)│ │(SERP Data) │  │(Scoring)        │  │
│  └──────┬───────┘  └─────┬───────┘  └────┬───────┘  └────────┬─────────┘  │
│         │                │               │                   │            │
│         └────────────────┴───────────────┴───────────────────┘            │
│                              │                                             │
│                    WorkflowContext (API client)                            │
└────────────────────────────────┬──────────────────────────────────────────┘
                                 │ HTTP REST API
                    ┌────────────▼──────────────┐
                    │    FastAPI Backend        │
                    │   (Async/Await Pattern)   │
                    └────────────┬──────────────┘
                                 │
          ┌──────────────────────┼──────────────────────┐
          │                      │                      │
    ┌─────▼─────┐          ┌─────▼─────┐         ┌─────▼──────┐
    │ Routers   │          │ Agents    │         │ Services   │
    │           │          │ Layer     │         │            │
    │• blog.py  │          │           │         │• groq_svc  │
    │• keywords │          │ 8 Agents  │         │• hashnode  │
    │• serp.py  │          │ (Modular) │         │• scraper   │
    │• seo.py   │          │           │         │            │
    └─────┬─────┘          └─────┬─────┘         └─────┬──────┘
          │                      │                      │
          └──────────┬───────────┴──────────┬───────────┘
                     │                      │
           ┌─────────▼──────────┐   ┌──────▼─────────┐
           │  Groq LLM Service  │   │  MongoDB       │
           │llama-3.3-70b-vers. │   │ (Persistence)  │
           │ (JSON Mode)        │   │                │
           └────────────────────┘   └────────────────┘
```

### Data Flow (Blog Generation Workflow)

```
User Input (Keyword, Toggles)
    │
    ├─→ Step 0: Web Search [Optional]
    │   └─→ Query DuckDuckGo → Fetch pages → LLM insights extraction
    │
    ├─→ Step 1: Keyword Clustering
    │   └─→ Intent-based clustering + traffic estimation
    │
    ├─→ Step 2: SERP Gap Analysis [Optional]
    │   └─→ DuckDuckGo SERP scrape → Competitor page parsing
    │   └─→ Content gap identification + missing keywords
    │
    ├─→ Step 3: Blog Generation
    │   └─→ Combined prompt (keywords + SERP gaps + web search)
    │   └─→ Stream blog content from Groq
    │
    ├─→ Step 4: AI Detection
    │   └─→ Perplexity + burstiness scoring (heuristic)
    │
    ├─→ Step 5: Humanization
    │   └─→ Conversational layer + AI-detection avoidance
    │
    ├─→ Step 6: SEO Audit
    │   └─→ Keyword density, readability, heading structure
    │
    ├─→ Step 7: Featured Snippet Optimization
    │   └─→ 3-variant generation (paragraph/list/table)
    │
    └─→ Step 8: Internal Linking
        └─→ Semantic anchor text + placement suggestions
        └─→ Save to MongoDB + Hashnode publication

Generated Blog (+ Metadata)
```

---

## Technology Stack

### Backend
| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Framework** | FastAPI | 0.100+ | Async REST API, automatic OpenAPI docs |
| **LLM Provider** | Groq | llama-3.3-70b-versatile | Primary generative model (JSON mode support) |
| **Database** | MongoDB | 4.4+ | Blog persistence, history tracking |
| **Async Driver** | Motor | 3.0+ | Async MongoDB client |
| **Validation** | Pydantic | v2 | Request/response schemas with validation |
| **Web Scraping** | BeautifulSoup4 + aiohttp | 4.11+ | DuckDuckGo SERP scraping, concurrency |
| **HTTP Client** | aiohttp | 3.8+ | Async HTTP (fetch competitor pages) |
| **Utilities** | python-dotenv | 0.20+ | Environment variable management |

### Frontend
| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Framework** | React | 18.0+ | UI components, state management |
| **Build Tool** | Vite | 4.0+ | Fast HMR development server |
| **Markdown** | react-markdown | 8.0+ | Render blog markdown |
| **HTTP Client** | Custom API client | - | Axios-like wrapper for backend calls |
| **Styling** | CSS Modules + inline | - | Component-scoped + dynamic styling |
| **State** | WorkflowContext | - | Global workflow state management |

### Infrastructure (Deployment Ready)
| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Container** | Docker | Containerized backend deployment |
| **Web Server** | Render | Platform as a Service (PaaS) deployment |
| **External APIs** | Hashnode API | Blog publication |
| **External APIs** | Groq Cloud | LLM inference |

---

## 8-Step Blog Generation Pipeline

### Step 0: Web Search (Optional)
**File:** `Backend/agents/web_search_agent.py`

**Purpose:** Fetch real-time web information and extract actionable insights for fresh, current content.

**Input:**
- `keyword`: User-provided topic
- `max_results`: Number of search results (default 8)
- `extract_insights`: Boolean to enable LLM insight extraction

**Process:**
1. Query DuckDuckGo HTML (no API key required)
2. Parse search results (title, URL, snippet)
3. Fetch full text from top 4 competitor pages (aiohttp concurrent)
4. Extract entities, statistics, and trends using Groq LLM
5. Identify key sources and trending topics

**Output:**
```python
{
  "keyword": str,
  "search_date": datetime,
  "results_count": int,
  "search_results": [{"url": str, "title": str, "snippet": str, ...}],
  "key_insights": [str],        # LLM-extracted insights
  "trending_topics": [str],     # Related topics from web
  "statistics": [str],          # Numbers/facts found
  "key_sources": [str]          # Authority domains
}
```

### Step 1: Keyword Clustering
**File:** `Backend/agents/keyword_agent.py`

**Purpose:** Generate intent-based keyword clusters with traffic + difficulty estimates.

**Input:**
```python
{
  "keyword": str,
  "secondary_keywords": List[str]
}
```

**Output:**
```python
{
  "clusters": [
    {
      "cluster_name": str,
      "intent": "informational|commercial|navigational|transactional",
      "keywords": List[str],
      "estimated_monthly_searches": str,
      "difficulty": "easy|medium|hard",
      "priority_score": float  # 0-1
    }
  ],
  "recommended_primary": str,
  "traffic_potential": "low|medium|high|very-high"
}
```

### Step 2: SERP Gap Analysis (Optional)
**File:** `Backend/agents/serp_agent.py`

**Purpose:** Competitive analysis — identify content gaps in top 10 SERP results.

**Input:**
```python
{
  "keyword": str,
  "competitor_urls": Optional[List[str]],
  "max_results": int = 10
}
```

**Process:**
1. Fetch DuckDuckGo SERP (top 10 results)
2. Extract metadata: title, URL, snippet, content type
3. Fetch full competitor pages (concurrently)
4. Parse headings, keywords, word count
5. Send to LLM for gap analysis
6. Compute missing keywords + weak sections (with heuristic fallback)

**Output:**
```python
{
  "serp_personality": str,      # e.g., "long-form"
  "results": [SERPResult],
  "content_gaps": [SERPGap],
  "missing_keywords": List[str],
  "weak_sections": List[str],
  "content_gap_summary": {
    "title": str,
    "description": str
  },
  "average_word_count": int,
  "recommended_word_count": int,
  "winning_angle": str
}
```

### Step 3: Blog Generation
**File:** `Backend/agents/blog_generator.py`

**Purpose:** Generate SEO-optimized blog content synthesis.

**Input:**
```python
{
  "keyword": str,
  "web_search_data": Optional[dict],      # From Step 0
  "serp_analysis": Optional[SERPAnalysis],# From Step 2
  "word_count": int,
  "tone": str,                             # "professional|casual|technical"
  "secondary_keywords": List[str]
}
```

**Process:**
1. Build comprehensive system prompt with all context
2. Generate markdown-formatted blog content
3. Include "LATEST WEB INFORMATION" section if web search enabled
4. Respect user word count (vs. SERP recommendation)

**Output:**
```python
{
  "title": str,
  "meta_description": str,
  "slug": str,
  "content": str,  # Markdown
  "word_count": int
}
```

### Step 4: AI Detection
**File:** `Backend/services/ai_detection_service.py`

**Purpose:** Detect AI-generated patterns and naturalness scoring.

**Input:** Blog content (string)

**Heuristic Scoring:**
- **Burstiness:** Variance of sentence length (high = more human-like)
- **Perplexity:** Ratio of unique words to total words
- **AI Phrase Flags:** Count of common AI patterns ("In conclusion," "As an AI," etc.)

**Output:**
```python
{
  "ai_probability_percent": float,  # 0-100
  "naturalness_score": float,       # 0-100
  "burstiness_score": float,        # 0-100
  "perplexity_indicator": str,      # "high|medium|low"
  "flags": List[str],               # Detected AI patterns
  "verdict": str                    # "likely_human|likely_ai|unclear"
}
```

### Step 5: Humanization
**File:** `Backend/agents/humanizer.py`

**Purpose:** Add conversational layer to reduce AI detection probability.

**Input:** Blog content

**Process:**
1. Rewrite introduction + conclusion with personal tone
2. Convert passive voice → active voice
3. Add rhetorical questions + transitions
4. Inject colloquialism (vary safely)
5. Reduce pattern repetition

**Output:** Humanized blog content (markdown)

### Step 6: SEO Optimization Audit
**File:** `Backend/agents/seo_optimizer.py`

**Purpose:** Analyze SEO metrics and provide actionable recommendations.

**Input:**
```python
{
  "content": str,
  "keyword": str,
  "secondary_keywords": Optional[List[str]]
}
```

**Metrics Computed:**
- **Keyword Density:** Optimal range 1-2.5% for primary keyword
- **Readability:** Flesch Reading Ease (40-60 = college level)
- **Structure:** Heading hierarchy (H1, H2, H3 balance)
- **LSI Keywords:** Related terms for semantic richness
- **Word Count:** Target vs. actual
- **Meta Description:** Length 150-160 chars

**Output:**
```python
{
  "overall_score": float,           # 0-100
  "keyword_density": [KeywordDensityDetail],
  "readability_score": float,
  "readability_grade": str,
  "word_count": int,
  "heading_count": int,
  "has_meta_structure": bool,
  "recommendations": List[str],
  "projected_traffic_potential": "low|medium|high|very-high",
  "issues": List[str]
}
```

### Step 7: Featured Snippet Optimization
**File:** `Backend/agents/snippet_agent.py`

**Purpose:** Generate featured snippet variants (Google SERP position 0).

**Input:**
```python
{
  "content": str,
  "keyword": str,
  "word_count": int
}
```

**Variants Generated:**
1. **Paragraph:** Concise summary (40-60 words)
2. **List:** Bullet-point format (5-7 items)
3. **Table:** Structured data comparison

**Scoring:**
- Length compliance (snippet correct bytes)
- Keyword inclusion
- Readability (avg word length < 5)

**Output:**
```python
{
  "recommended_variant": SnippetVariant,
  "all_variants": [SnippetVariant],
  "readiness_probability": float,    # 0-100
  "optimization_tips": List[str]
}
```

### Step 8: Internal Linking
**File:** `Backend/agents/internal_linking_agent.py`

**Purpose:** Generate contextual internal link suggestions.

**Input:**
```python
{
  "content": str,
  "keyword": str,
  "available_blogs": Optional[List[BlogMetadata]]
}
```

**Process:**
1. Identify contexts suitable for internal links
2. Generate semantic anchor text (avoid "click here")
3. Suggest placement within blog structure
4. Provide relevance scoring

**Output:**
```python
{
  "total_suggestions": int,
  "suggestions": [
    {
      "anchor_text": str,
      "target_url": str,
      "target_title": str,
      "relevance_score": float,
      "placement_hint": str,
      "reason": str
    }
  ],
  "linking_score": float
}
```

---

## API Endpoints & Specifications

### Master Endpoint: Generate Blog
**POST `/blog/generate`**

Orchestrates the entire 8-step pipeline in sequence.

**Request:**
```json
{
  "keyword": "string (required)",
  "secondary_keywords": ["string"],
  "word_count": 2500,
  "tone": "professional|casual|technical",
  "enable_web_search": true,
  "enable_serp_analysis": true,
  "competitor_urls": ["https://..."],
  "publish_to_hashnode": false,
  "hashnode_publication_id": "optional_string"
}
```

**Response (202 Accepted):**
```json
{
  "blog_id": "uuid",
  "keyword": "string",
  "blog": {
    "title": "string",
    "meta_description": "string",
    "slug": "string",
    "content": "markdown",
    "word_count": 2500
  },
  "web_search": {
    "search_date": "iso8601",
    "results_count": 8,
    "key_insights": ["string"],
    "trending_topics": ["string"]
  },
  "keywords": {
    "clusters": [...]
  },
  "serp_analysis": {
    "winning_angle": "string",
    "missing_keywords": ["string"],
    "weak_sections": ["string"],
    "recommended_word_count": 2500
  },
  "ai_detection": {
    "ai_probability_percent": 15.5,
    "naturalness_score": 84.3,
    "verdict": "likely_human"
  },
  "seo_audit": {
    "overall_score": 87,
    "recommendations": ["string"]
  },
  "snippet": {
    "recommended_variant": {...},
    "readiness_probability": 72.5
  },
  "internal_links": {
    "total_suggestions": 3,
    "suggestions": [...]
  },
  "hashnode_result": {
    "success": true,
    "hashnode_url": "string"
  },
  "execution_time_ms": 45000
}
```

### Individual Endpoints

#### 1. Keyword Clustering
**POST `/keywords/cluster`**
```json
Request: { "keyword": str, "secondary_keywords": [str] }
Response: KeywordClusterResponse
```

#### 2. SERP Gap Analysis
**POST `/serp/analyze`**
```json
Request: { "keyword": str, "competitor_urls": [str] }
Response: SERPAnalysisResponse
```

#### 3. Blog Generation
**POST `/blog`** (without pipeline)
```json
Request: { "keyword": str, "word_count": int, "tone": str }
Response: BlogGenerationResponse
```

#### 4. SEO Audit
**POST `/seo/analyze`**
```json
Request: { "content": str, "keyword": str }
Response: SEOScoreResponse
```

#### 5. AI Detection
**POST `/seo/detect-ai`**
```json
Request: { "content": str }
Response: AIDetectionResponse
```

#### 6. Featured Snippet Optimization
**POST `/seo/snippet`**
```json
Request: { "content": str, "keyword": str }
Response: SnippetOptimizationResponse
```

#### 7. Internal Linking
**POST `/seo/links`**
```json
Request: { "content": str, "keyword": str }
Response: InternalLinkResponse
```

#### 8. Humanization
**POST `/humanize`**
```json
Request: { "content": str }
Response: { "humanized_content": str, "tone_detected": str }
```

---

## Data Models

### Request Models (`Backend/models/request_models.py`)
```python
class BlogGenerationRequest(BaseModel):
    keyword: str = Field(..., min_length=1, max_length=100)
    secondary_keywords: List[str] = DEFAULT_SECONDARY_KEYWORDS
    word_count: int = Field(2500, ge=500, le=10000)
    tone: str = "professional"
    enable_web_search: bool = True
    enable_serp_analysis: bool = True
    competitor_urls: List[str] = []
    publish_to_hashnode: bool = False
    hashnode_publication_id: Optional[str] = None
```

### Response Models (`Backend/models/response_models.py`)
```python
class BlogGenerationResponse(BaseModel):
    title: str
    meta_description: str
    slug: str
    content: str
    word_count: int
    blog_id: Optional[str]
    created_at: Optional[datetime]
    hashnode_url: Optional[str]

class SEOScoreResponse(BaseModel):
    overall_score: float
    keyword_density: List[KeywordDensityDetail]
    readability_score: float
    readability_grade: str
    word_count: int
    heading_count: int
    has_meta_structure: bool
    internal_link_count: int
    keyword_in_title: bool
    keyword_in_first_100_words: bool
    lsi_keywords_found: List[str]
    issues: List[str]
    recommendations: List[str]
    projected_traffic_potential: str

class SERPAnalysisResponse(BaseModel):
    keyword: str
    serp_personality: str
    results: List[SERPResult]
    content_gaps: List[SERPGap]
    missing_keywords: List[str]
    weak_sections: List[str]
    content_gap_summary: ContentGapSummary
    average_word_count: int
    recommended_word_count: int
    winning_angle: str
```

---

## Database Schema

### MongoDB Collections

#### blogs
```javascript
{
  "_id": ObjectId,
  "keyword": String,
  "title": String,
  "content": String,
  "meta_description": String,
  "slug": String,
  "word_count": Number,
  "tone": String,
  
  // Metadata
  "created_at": Date,
  "updated_at": Date,
  "generated_by_agent_version": String,
  
  // SEO Metrics
  "seo_score": Number,
  "keyword_density": [{keyword: String, density: Number}],
  "readability_score": Number,
  "ai_probability_percent": Number,
  
  // Associations
  "web_search_data": Object,
  "serp_analysis": Object,
  "internal_links": [ObjectId],
  
  // Publication
  "published_to_hashnode": Boolean,
  "hashnode_id": String,
  "hashnode_url": String,
  
  // Audit Trail
  "steps_executed": [String],
  "execution_time_ms": Number,
  "user_id": Optional[String]
}
```

#### serp_cache
```javascript
{
  "_id": ObjectId,
  "keyword": String,
  "serp_results": [Object],
  "analysis": Object,
  "fetched_at": Date,
  "ttl_expires_at": Date
}
```

#### web_search_cache
```javascript
{
  "_id": ObjectId,
  "keyword": String,
  "search_results": [Object],
  "insights": [String],
  "fetched_at": Date,
  "ttl_expires_at": Date
}
```

---

## Feature Specifications

### Feature 1: Real-Time Web Search Integration
- **Status:** ✅ Implemented
- **Toggle:** `enable_web_search` (boolean)
- **Latency:** 3-5 seconds (async concurrent)
- **Data Sources:** DuckDuckGo HTML scraping
- **Insights Extraction:** Groq LLM JSON mode
- **Output:** Integrated into blog prompt context

### Feature 2: Competitor SERP Analysis
- **Status:** ✅ Implemented
- **Toggle:** `enable_serp_analysis` (boolean)
- **Competitors Analyzed:** Top 10 results
- **Content Gaps:** Missing keywords + weak sections
- **Heuristic Fallback:** Enabled for LLM failures
- **Output:** Gap summary + winning angle

### Feature 3: AI Humanization Layer
- **Status:** ✅ Implemented
- **Techniques:** 
  - Active voice conversion
  - Rhetorical question injection
  - Burstiness optimization (sentence variety)
  - Colloquialism addition (safe patterns)
- **Detection Score:** Naturalness 0-100

### Feature 4: SEO Audit Suite
- **Status:** ✅ Implemented
- **Metrics:**
  - Keyword density compliance
  - Readability grade (Flesch)
  - Heading structure analysis
  - Internal link recommendations
  - Meta structure validation
  - Projected traffic potential

### Feature 5: Featured Snippet Optimization
- **Status:** ✅ Implemented
- **Variants:** Paragraph, List, Table
- **Scoring:** Length + readability + keyword inclusion
- **Readiness Probability:** 0-100%

### Feature 6: Internal Linking Engine
- **Status:** ✅ Implemented
- **Algorithm:** Semantic similarity + anchor text generation
- **Placement Hints:** Strategic positioning within content
- **Validation:** Relevance scoring (0-1)

### Feature 7: Hashnode Integration
- **Status:** ✅ Implemented
- **API:** REST endpoint for blog publication
- **Authentication:** API Key from .env
- **Output:** Hashnode URL + blog ID tracking

### Feature 8: User-Controlled Parameters
- **Status:** ✅ Implemented
- **Controls:**
  - `word_count`: 500-10,000 words (user overrides SERP recommendation)
  - `tone`: professional | casual | technical
  - `enable_web_search`: Toggle real-time content
  - `enable_serp_analysis`: Toggle competitive analysis
  - `publish_to_hashnode`: Auto-publish option

---

## Setup & Deployment

### Prerequisites
- Python 3.9+
- Node.js 16+
- MongoDB 4.4+
- Groq API Key
- Hashnode API Key (optional)

### Backend Setup

```bash
# 1. Environment variables
cp Backend/.env.example Backend/.env
# Edit .env with credentials

# 2. Install Python dependencies
pip install -r Backend/requirements.txt

# 3. Start FastAPI server
cd Backend
python -m uvicorn core.main:app --reload --port 8000

# 4. Database: Ensure MongoDB is running
# Local: mongod
# Cloud: MongoDB Atlas connection string in .env
```

### Frontend Setup

```bash
# 1. Install dependencies
cd frontend
npm install

# 2. Start Vite dev server
npm run dev

# 3. Build for production
npm run build

# 4. Preview production build
npm run preview
```

### Environment Variables (`.env`)

```bash
# Backend/.env
GROQ_API_KEY=your_groq_key_here
MONGO_URI=mongodb://localhost:27017 or MongoDB Atlas URI
HASHNODE_API_KEY=your_hashnode_key_here
HASHNODE_PUBLICATION_ID=your_pub_id

# Frontend/.env
VITE_API_URL=http://localhost:8000/api
```

### Docker Deployment

```dockerfile
# Dockerfile (Backend)
FROM python:3.11-slim
WORKDIR /app
COPY Backend/requirements.txt .
RUN pip install -r requirements.txt
COPY Backend .
CMD ["uvicorn", "core.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# Build & run
docker build -t blogy-backend .
docker run -p 8000:8000 --env-file .env blogy-backend
```

---

## Performance & Optimization

### Execution Timeline
| Step | Time (seconds) | Status |
|------|---|---|
| Web Search | 3-5 | Optional |
| Keyword Clustering | 2-3 | Always |
| SERP Analysis | 5-8 | Optional |
| Blog Generation | 15-20 | Always |
| AI Detection | 1-2 | Always |
| Humanization | 3-5 | Always |
| SEO Audit | 1-2 | Always |
| Snippet Opt. | 2-3 | Always |
| Internal Links | 2-3 | Always |
| **Total (Full)** | **35-50 seconds** | - |
| **Total (No SERP/Web)** | **27-37 seconds** | - |

### Optimization Strategies
1. **Async Concurrency:** All I/O operations use `asyncio.gather()`
2. **Page Fetching:** Concurrent HTTP requests (4 concurrent connections)
3. **LLM Batching:** Group prompts when possible
4. **Caching:** SERP results cached with TTL (24 hours)
5. **Streaming:** Frontend receives blog chunks progressively
6. **Heuristic Fallback:** LLM failures don't break pipeline

### Scalability Considerations
- **Stateless Agents:** Each agent is independent, can be parallelized
- **Database Indexing:** Indexes on `keyword`, `created_at`, `blog_id`
- **Rate Limiting:** Groq queue (planned) + exponential backoff
- **Load Balancing:** FastAPI behind load balancer (Nginx/HAProxy)
- **Horizontal Scaling:** MongoDB replica set recommended for production

---

## Debugging & Monitoring

### Logs Location
- **Backend:** `Backend/debug/` (optional debug logs)
- **Frontend:** Browser console + Network tab

### Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| "GROQ_API_KEY not found" | Missing .env | Create `.env` with valid key |
| MongoDB connection error | MongoDB not running | Start `mongod` or check Atlas URI |
| Blog generation timeout (>60s) | SERP analysis too slow | Disable `enable_serp_analysis` |
| "[object Object]" in SERP insights | Response format mismatch | Check `content_gap_summary` model |
| Type errors in Groq response | Mixed types in join() | All join operations use `str()` conversion |

---

## Git workflow

```bash
# Pull latest
git pull origin main

# Create feature branch
git checkout -b feature/your-feature

# Commit changes
git add .
git commit -m "feat: description"

# Push & create PR
git push origin feature/your-feature
```

---

## License & Credits

Built with ❤️ for Bizmark'26 Hackathon.
- **LLM:** Groq (llama-3.3-70b-versatile)
- **Platform:** FastAPI + React
- **Database:** MongoDB

---

## Quick Start

### 1. Clone & Install

```bash
git clone <repo>
cd blogy-ai-engine

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

### 2. Configure

```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

### 3. Run

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Open: http://localhost:8000/docs

---

## API Reference

### POST `/blog/generate` — Full Pipeline

```json
{
  "keyword": "AI blog automation tool India",
  "secondary_keywords": ["blog automation", "SEO tool India", "AI content writer"],
  "target_location": "India",
  "word_count": 2500,
  "tone": "professional",
  "competitor_urls": [],
  "internal_links": [
    {
      "title": "How to Rank on Google in India",
      "url": "https://blogy.in/blog/rank-google-india",
      "topic": "SEO",
      "keywords": ["SEO", "Google ranking India"]
    }
  ],
  "enable_humanization": true
}
```

**Response includes:**
- `title`, `meta_description`, `slug`, `content`
- `seo_score` — Full SEO audit (0-100)
- `ai_detection` — AI probability + naturalness + flags
- `snippet_optimization` — 3 snippet variants + readiness score
- `internal_links` — Semantic link suggestions
- `keyword_clusters` — Intent-grouped keyword clusters
- `serp_analysis` — Competitor gaps + winning angle
- `generation_time_seconds`

---

### POST `/keywords/cluster`

```json
{
  "seed_keyword": "SEO tool",
  "target_location": "India",
  "cluster_count": 5
}
```

### POST `/serp/analyze`

```json
{
  "keyword": "best AI blog automation tool India",
  "target_location": "India",
  "max_results": 10
}
```

### POST `/seo/analyze`

```json
{
  "content": "# Your blog content here...",
  "keyword": "AI blog automation",
  "secondary_keywords": ["blog tool", "SEO automation"]
}
```

### POST `/seo/detect-ai`

```json
{
  "content": "Your blog content to check for AI patterns..."
}
```

### POST `/seo/snippet`

```json
{
  "content": "# Blog content...",
  "keyword": "AI blog automation tool"
}
```

### POST `/seo/links`

```json
{
  "content": "# Blog content...",
  "primary_keyword": "AI blog automation",
  "existing_blogs": [
    {
      "title": "How to Rank on Google",
      "url": "https://blogy.in/blog/rank-google",
      "topic": "SEO",
      "keywords": ["SEO", "Google ranking"]
    }
  ]
}
```

### POST `/humanize`

```json
{
  "content": "# AI-generated blog content...",
  "force": false
}
```

---

## AI Detection Algorithm

The heuristic AI detector doesn't need a paid API. It scores on 4 signals:

| Signal | Weight | What it measures |
|---|---|---|
| **Burstiness** | 35% | Sentence length variance — AI writes uniform lengths |
| **Perplexity Proxy** | 25% | Bigram uniqueness ratio — AI reuses transitions |
| **AI Phrase Flags** | 30% | 20 known AI clichés ("delve into", "in today's world", etc.) |
| **Paragraph Uniformity** | 10% | AI paragraphs are suspiciously equal in length |

---

## SEO Score Breakdown

| Component | Max Points | How |
|---|---|---|
| Word count ≥ 2,500 | 20 | Full marks for 2500+, partial for 1500+ |
| Keyword density 0.5-2.5% | 20 | Optimal range = full marks |
| Readability ≥ 60 | 15 | Flesch-Kincaid score |
| Headings ≥ 5 | 10 | H2/H3 structure |
| Keyword in title | 15 | Binary check |
| Keyword in first 100 words | 10 | Binary check |
| Internal links ≥ 3 | 5 | Markdown link count |
| LSI keywords ≥ 8 | 5 | Top co-occurring non-stopword terms |
| **Total** | **100** | |

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | ✅ | Get from console.groq.com |
| `SERPAPI_KEY` | ❌ | Optional (uses DuckDuckGo scraper by default) |
| `APP_ENV` | ❌ | `development` / `production` |
| `APP_HOST` | ❌ | Default: `0.0.0.0` |
| `APP_PORT` | ❌ | Default: `8000` |
| `CORS_ORIGINS` | ❌ | Comma-separated frontend origins |
