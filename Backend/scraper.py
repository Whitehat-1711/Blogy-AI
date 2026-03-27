"""
Scraper utility — fetches DuckDuckGo HTML SERP results + individual page content.
No API key needed. Falls back gracefully on network errors.
"""

import re
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from config import SCRAPER_TIMEOUT, MAX_SERP_RESULTS


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


async def _fetch(session: aiohttp.ClientSession, url: str, timeout: int = SCRAPER_TIMEOUT) -> str:
    try:
        async with session.get(url, headers=HEADERS, timeout=aiohttp.ClientTimeout(total=timeout)) as resp:
            if resp.status == 200:
                return await resp.text()
    except Exception:
        pass
    return ""


async def get_serp_results(keyword: str, max_results: int = MAX_SERP_RESULTS) -> list[dict]:
    """
    Scrape DuckDuckGo for top organic results.
    Returns list of { title, url, snippet }.
    """
    query = keyword.replace(" ", "+")
    url = f"https://html.duckduckgo.com/html/?q={query}&kl=in-en"

    async with aiohttp.ClientSession() as session:
        html = await _fetch(session, url)

    if not html:
        return []

    soup = BeautifulSoup(html, "lxml")
    results = []

    for result in soup.select(".result__body")[:max_results]:
        title_tag = result.select_one(".result__title a")
        snippet_tag = result.select_one(".result__snippet")
        url_tag = result.select_one(".result__url")

        if not title_tag:
            continue

        title = title_tag.get_text(strip=True)
        link = title_tag.get("href", "")
        snippet = snippet_tag.get_text(strip=True) if snippet_tag else ""
        display_url = url_tag.get_text(strip=True) if url_tag else link

        # DuckDuckGo wraps links — clean them
        if link.startswith("//duckduckgo.com/l/"):
            m = re.search(r"uddg=([^&]+)", link)
            if m:
                from urllib.parse import unquote
                link = unquote(m.group(1))

        results.append({"title": title, "url": link, "snippet": snippet, "display_url": display_url})

    return results


async def fetch_page_text(url: str) -> str:
    """
    Download a URL and return its cleaned body text.
    Used to estimate competitor word counts and extract topics.
    """
    async with aiohttp.ClientSession() as session:
        html = await _fetch(session, url, timeout=15)

    if not html:
        return ""

    soup = BeautifulSoup(html, "lxml")

    # Remove scripts, styles, nav, footer
    for tag in soup(["script", "style", "nav", "footer", "header", "aside", "form"]):
        tag.decompose()

    # Prefer article / main body
    body = soup.find("article") or soup.find("main") or soup.find("body")
    if body:
        return " ".join(body.get_text(separator=" ").split())
    return " ".join(soup.get_text(separator=" ").split())


async def fetch_multiple_pages(urls: list[str]) -> list[str]:
    """Concurrently fetch multiple pages."""
    tasks = [fetch_page_text(url) for url in urls]
    return await asyncio.gather(*tasks)
