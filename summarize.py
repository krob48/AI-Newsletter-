# summarize.py
from typing import Optional
import os

def summarize_fallback(title: str, body: str) -> str:
    """
    No-OpenAI fallback: return 3 short bullets from the first ~500 chars.
    This lets you demo without any AI key.
    """
    snippet = (body or "").strip().split(". ")
    bullets = []
    for s in snippet[:3]:
        s = s.strip()
        if not s: 
            continue
        # Keep it short
        if len(s) > 160:
            s = s[:157] + "..."
        bullets.append(f"- {s}")
    if not bullets:
        bullets = [f"- {title}: (no content available)"]
    return "\n".join(bullets)

def summarize_with_openai(openai_api_key: str, title: str, body: str) -> str:
    """
    Uses OpenAI (one single API key) to produce crisp bullets.
    """
    if not openai_api_key:
        return summarize_fallback(title, body)

    try:
        from openai import OpenAI
        client = OpenAI(api_key=openai_api_key)
        prompt = f"""
Summarize the article titled "{title}" into 3–5 concise bullets for a newsletter.
Use neutral tone; each bullet under 22 words.
Article:
{body[:8000]}
"""
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You write crisp, factual bullet summaries."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
        )
        return resp.choices[0].message.content.strip() or summarize_fallback(title, body)
    except Exception:
        # If anything fails, fall back gracefully
        return summarize_fallback(title, body)
