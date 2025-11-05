# test_fetch.py
from config import GUARDIAN_API_KEY
from fetch import search_articles, get_article_body

assert GUARDIAN_API_KEY, "Missing GUARDIAN_API_KEY. Put it in .env."

arts = search_articles(GUARDIAN_API_KEY, ["ai", "technology"], page_size=3)
for a in arts:
    print("Headline:", a["headline"])
    print("URL:", a["webUrl"])
    body = get_article_body(GUARDIAN_API_KEY, a["id"])
    print("Body first 200 chars:", body[:200].replace("\n", " "), "...\n")
