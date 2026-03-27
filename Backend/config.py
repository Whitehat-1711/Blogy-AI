import os
from dotenv import load_dotenv

load_dotenv()

# ── Groq ──────────────────────────────────────────────────────────────────────
GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL: str = "llama-3.3-70b-versatile"
GROQ_MAX_TOKENS: int = 8000
GROQ_TEMPERATURE: float = 0.7

# ── SerpAPI (optional – fallback to scraper if missing) ──────────────────────
SERPAPI_KEY: str = os.getenv("SERPAPI_KEY", "")

# ── App ───────────────────────────────────────────────────────────────────────
APP_ENV: str = os.getenv("APP_ENV", "development")
APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT: int = int(os.getenv("APP_PORT", "8000"))
CORS_ORIGINS: list[str] = os.getenv(
    "CORS_ORIGINS", "http://localhost:3000,http://localhost:5173"
).split(",")

# ── SEO thresholds ────────────────────────────────────────────────────────────
KEYWORD_DENSITY_MIN: float = 0.5   # %
KEYWORD_DENSITY_MAX: float = 2.5   # %
MIN_WORD_COUNT: int = 1500
IDEAL_WORD_COUNT: int = 2500

# ── Scraper ───────────────────────────────────────────────────────────────────
SCRAPER_TIMEOUT: int = 10
MAX_SERP_RESULTS: int = 10
