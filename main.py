# main.py
from datetime import datetime
import argparse
import webbrowser
from pathlib import Path
from typing import List, Dict, Optional
import os

from config import GUARDIAN_API_KEY, OPENAI_API_KEY, DEFAULT_TOPICS, MAX_ARTICLES
from fetch import search_articles, get_article_body
from summarize import summarize_with_openai
from render import build_html
from emailer import send_email


def run(
    topics: List[str],
    max_articles: int,
    to_addr: Optional[str],
    subject: str = "AI Newsletter",
    no_open: bool = False,
) -> None:
    assert GUARDIAN_API_KEY, "Missing GUARDIAN_API_KEY in .env"

    Path("out").mkdir(exist_ok=True)

    # 1) Fetch article metadata
    results = search_articles(
        api_key=GUARDIAN_API_KEY,
        topics=topics,
        page_size=max_articles
    )

    # 2) Fetch bodies + summarize
    items: List[Dict] = []
    for a in results:
        body = get_article_body(GUARDIAN_API_KEY, a["id"])
        summary = summarize_with_openai(OPENAI_API_KEY, a["headline"], body)
        items.append({
            "headline": a["headline"],
            "url": a["webUrl"] or a["shortUrl"],
            "summary": summary,
        })

    # 3) Render HTML (timestamped filename)
    out_path = Path(f"out/newsletter_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.html")
    html = build_html(items)
    out_path.write_text(html, encoding="utf-8")
    print(f"[render] wrote {out_path.resolve()}")

    # 4) Open locally for inspection (only if not disabled)
    if not no_open:
        webbrowser.open(f"file://{out_path.resolve()}")
    else:
        print("[open] Skipped opening browser (--no_open flag set)")

    # 5) Email (only if recipient provided)
    if to_addr:
        smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        smtp_user = os.getenv("SMTP_USER", "")
        smtp_password = os.getenv("SMTP_PASSWORD", "")
        from_name = os.getenv("FROM_NAME", "AI Newsletter")
        from_email = os.getenv("FROM_EMAIL", smtp_user)

        missing = [k for k, v in {
            "SMTP_USER": smtp_user,
            "SMTP_PASSWORD": smtp_password,
            "FROM_EMAIL": from_email
        }.items() if not v]
        if missing:
            print(f"[email] Missing SMTP config: {', '.join(missing)}. Add them to your .env.")
        else:
            try:
                print(f"[email] sending to {to_addr} via {smtp_host}:{smtp_port} as {from_email}")
                send_email(
                    smtp_host=smtp_host, smtp_port=smtp_port,
                    smtp_user=smtp_user, smtp_password=smtp_password,
                    from_name=from_name, from_email=from_email,
                    to_email=to_addr, subject=subject, html_body=html
                )
                print("[email] sent.")
            except Exception as e:
                print(f"[email] ERROR: {e}")
    else:
        print("[email] No recipient (--to or TO_EMAIL in .env) provided; skipping send.")

    print(f"[done] Output: {out_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Newsletter")
    parser.add_argument("--topics", type=str, default=",".join(DEFAULT_TOPICS),
                        help='Comma-separated topics (e.g., "ai,technology")')
    parser.add_argument("--max_articles", type=int, default=MAX_ARTICLES)
    parser.add_argument("--to", type=str, default="",
                        help="Recipient email address")
    parser.add_argument("--subject", type=str, default="AI Newsletter",
                        help="Subject line for the email")
    parser.add_argument("--no_open", action="store_true",
                        help="If set, do not open the newsletter in a browser (useful for cron jobs)")

    args = parser.parse_args()

    # Allow default recipient from .env
    default_to = os.getenv("TO_EMAIL", "")
    to_addr = args.to or (default_to if default_to.strip() else None)

    topics = [t.strip() for t in args.topics.split(",") if t.strip()]
    run(
        topics=topics,
        max_articles=args.max_articles,
        to_addr=to_addr,
        subject=args.subject,
        no_open=args.no_open,
    )

