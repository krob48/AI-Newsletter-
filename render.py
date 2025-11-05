# render.py
from typing import List, Dict
from datetime import datetime
import html

def build_html(items: List[Dict]) -> str:
    now = datetime.now().strftime("%B %d, %Y %I:%M %p")
    blocks = []
    for it in items:
        headline = html.escape(it["headline"])
        url = html.escape(it["url"])
        summary = html.escape(it["summary"])
        blocks.append(f"""
        <div style="margin-bottom:20px;padding-bottom:16px;border-bottom:1px solid #ddd;">
            <h3 style="margin:0 0 8px 0;font-family:Arial,sans-serif;">{headline}</h3>
            <div><a href="{url}" target="_blank">{url}</a></div>
            <pre style="white-space:pre-wrap;font-family:Inter,Arial,sans-serif;">{summary}</pre>
        </div>
        """)
    body = "\n".join(blocks) if blocks else "<p>No items.</p>"
    return f"""<!doctype html>
<html>
<head><meta charset="utf-8"><title>AI Newsletter</title></head>
<body style="max-width:720px;margin:24px auto;padding:0 16px;font-family:Arial,sans-serif;">
  <h1 style="margin-bottom:4px;">AI Newsletter</h1>
  <div style="color:#666;margin-bottom:20px;">Generated on {now}</div>
  {body}
</body>
</html>"""
