"""LinkedIn automation skill."""

from __future__ import annotations

import requests

from src.utils.vault import normalize_filename, task_header, write_task


def create_linkedin_draft(content: str) -> None:
    title = "LinkedIn post draft"
    filename = normalize_filename(f"linkedin_post_{content[:50]}")
    body = f"**LinkedIn draft**\n\n{content}\n"
    write_task("Needs_Action", filename, task_header(title) + body)


def post_linkedin(content: str) -> dict[str, str]:
    """Use MCP server to post to LinkedIn (requires credentials)."""
    url = "http://localhost:3000/linkedin-post"
    resp = requests.post(url, json={"content": content}, timeout=60)
    resp.raise_for_status()
    return resp.json()
