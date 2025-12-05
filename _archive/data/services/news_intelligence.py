import requests
import feedparser # type: ignore
from typing import Dict, Any, List

class NewsIntelligenceService:
    def fetch_google_news_rss(self, query: str = "pharma") -> List[Dict[str, Any]]:
        """
        Parses Google News RSS feed.
        """
        url = f"https://news.google.com/rss/search?q={query}"
        try:
            # Google News requires a User-Agent
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            feed = feedparser.parse(response.content)
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
            return [{"error": str(e)}]

    def fetch_gdelt(self, query: str = "pharmaceutical") -> Dict[str, Any]:
        """
        Fetches from GDELT Doc API.
        """
        url = "https://api.gdeltproject.org/api/v2/doc/doc"
        params = {
            "query": query,
            "mode": "artlist",
            "maxrecords": 5,
            "format": "json"
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}
