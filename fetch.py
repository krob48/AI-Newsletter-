# fetch.py
from typing import List, Dict, Any
import requests

GUARDIAN_SEARCH_URL = "https://content.guardianapis.com/search"
GUARDIAN_ITEM_URL = "https://content.guardianapis.com/{}"

def search_articles(api_key: str, topics: List[str], page_size: int = 10) -> List[Dict[str, Any]]:
    """
    Uses Python 'requests' to call The Guardian search endpoint.
    We OR-join the topics for a broader query.
    """
    if not topics:
        topics = ["ai"]
    query = " OR ".join(topics)

    params = {
        "api-key": api_key,
        "q": query,
        "order-by": "newest",
        "show-fields": "trailText,headline,shortUrl",
        "page-size": page_size
    }
    r = requests.get(GUARDIAN_SEARCH_URL, params=params, timeout=15)
    r.raise_for_status()
    data = r.json()
    results = data.get("response", {}).get("results", [])
    articles = []
    for item in results:
        fields = item.get("fields", {}) or {}
        articles.append({
            "id": item.get("id"),
            "webUrl": item.get("webUrl"),
            "headline": fields.get("headline") or item.get("webTitle"),
            "trailText": fields.get("trailText", ""),
            "shortUrl": fields.get("shortUrl", item.get("webUrl")),
        })
    return articles

def get_article_body(api_key: str, article_id: str) -> str:
    """
    Fetch full text (bodyText) for a specific article if available.
    """
    url = GUARDIAN_ITEM_URL.format(article_id)
    params = {
        "api-key": api_key,
        "show-fields": "headline,trailText,bodyText"
    }
    r = requests.get(url, params=params, timeout=15)
    r.raise_for_status()
    data = r.json()
    content = data.get("response", {}).get("content", {}) or {}
    fields = content.get("fields", {}) or {}
    return (fields.get("bodyText") or fields.get("trailText") or "").strip()
