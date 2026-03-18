"""Email sending skill using MCP server."""

from __future__ import annotations

import requests

from src.utils.vault import normalize_filename, task_header, write_task


def create_email_task(to: str, subject: str, body: str) -> None:
    title = f"Send email to {to}"
    filename = normalize_filename(f"email_{to}_{subject[:40]}")
    content = task_header(title, {"to": to, "subject": subject}) + body
    write_task("Needs_Action", filename, content)


def send_email(to: str, subject: str, text: str, html: str | None = None) -> dict:
    url = "http://localhost:3000/send-email"
    payload = {"to": to, "subject": subject, "text": text, "html": html}
    resp = requests.post(url, json=payload, timeout=60)
    resp.raise_for_status()
    return resp.json()
