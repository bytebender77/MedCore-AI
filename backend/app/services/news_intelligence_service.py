import aiohttp
import asyncio
import feedparser # type: ignore
from typing import Dict, Any, List
from ..core.config import get_settings

class NewsIntelligenceService:
    def __init__(self):
        self.settings = get_settings()
        self.timeout = aiohttp.ClientTimeout(total=30)

    async def fetch_google_news_rss(self, query: str = "pharma") -> Dict[str, Any]:
        """
        Parses Google News RSS feed.
        """
        if self.settings.DATA_MODE != "real":
             return {"articles": [{"source": {"name": "Mock News"}, "title": "Mock News Title", "description": "Mock Description", "url": "http://mock.url"}]}

        url = f"https://news.google.com/rss/search?q={query}"
        try:
            # Google News requires a User-Agent
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(url, headers=headers, ssl=False) as response:
                    if response.status != 200:
                        return {"error": f"Status {response.status}"}
                    
                    content = await response.text()
                    feed = feedparser.parse(content)
                    
                    articles = []
                    for entry in feed.entries[:5]:
                        articles.append({
                            "source": {"name": entry.get("source", {}).get("title") or "Google News"},
                            "title": entry.title,
                            "description": entry.get("summary") or entry.get("description"),
                            "url": entry.link
                        })
                    return {"articles": articles}
        except Exception as e:
            return {"error": str(e)}

    async def fetch_gdelt(self, query: str = "pharmaceutical") -> Dict[str, Any]:
        """
        Fetches from GDELT Doc API.
        """
        if self.settings.DATA_MODE != "real":
             return {"articles": [{"title": "Mock GDELT Article", "url": "http://mock.gdelt.url"}]}

        url = "https://api.gdeltproject.org/api/v2/doc/doc"
        params = {
            "query": query,
            "mode": "artlist",
            "maxrecords": 5,
            "format": "json"
        }
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(url, params=params, ssl=False) as response:
                    if response.status != 200:
                        return {"error": f"Status {response.status}"}
                    return await response.json()
        except Exception as e:
            return {"error": str(e)}
