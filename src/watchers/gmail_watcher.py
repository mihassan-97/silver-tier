"""Gmail watcher: detects new emails and creates tasks in Vault/Needs_Action.

This script uses the Gmail API via OAuth2. To set up:
1. Go to https://console.developers.google.com/
2. Create a project and enable the Gmail API.
3. Create OAuth client credentials (Desktop app) and download the JSON as `credentials.json`.
4. Place `credentials.json` in the project root (or set GMAIL_CREDENTIALS_PATH).

On first run, this script will open a browser to authorize and store a token at `state/gmail_token.json`.

Run:
    python -m src.watchers.gmail_watcher

"""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from src.config import settings
from src.utils.vault import normalize_filename, task_header, write_task

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
STATE_FILE = Path("state/gmail_state.json")


def load_state() -> dict[str, Any]:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {"seen_ids": []}


def save_state(state: dict[str, Any]) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def get_gmail_service() -> Any:
    creds = None
    cred_path = Path(settings.GMAIL_CREDENTIALS_PATH)
    token_path = Path(settings.GMAIL_TOKEN_PATH)

    if token_path.exists():
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(cred_path), SCOPES)
            creds = flow.run_local_server(port=0)
        token_path.parent.mkdir(parents=True, exist_ok=True)
        with open(token_path, "w", encoding="utf-8") as token:
            token.write(creds.to_json())

    service = build("gmail", "v1", credentials=creds)
    return service


def fetch_unread_messages(service: Any, user_id: str = "me") -> list[dict[str, Any]]:
    results = service.users().messages().list(userId=user_id, q="is:unread").execute()
    messages = results.get("messages", [])
    out = []
    for msg in messages:
        msg_data = service.users().messages().get(userId=user_id, id=msg["id"], format="full").execute()
        out.append(msg_data)
    return out


def parse_message(msg: dict[str, Any]) -> tuple[str, str]:
    headers = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}
    subject = headers.get("Subject", "(no subject)")
    from_header = headers.get("From", "(unknown sender)")
    snippet = msg.get("snippet", "")
    body = f"**From:** {from_header}\n\n**Subject:** {subject}\n\n---\n\n{snippet}\n"
    title = f"Email: {subject}"
    return title, body


def create_task_for_message(title: str, body: str) -> None:
    filename = normalize_filename(f"{datetime.utcnow().isoformat()}_{title}")
    content = task_header(title, {"created": datetime.utcnow().isoformat()}) + body
    write_task("Needs_Action", filename, content)


def main() -> None:
    service = get_gmail_service()
    new_messages = fetch_unread_messages(service, settings.GMAIL_USER_ID)
    if not new_messages:
        print("No new unread messages.")
        return

    state = load_state()
    seen_ids = set(state.get("seen_ids", []))
    created = 0
    for msg in new_messages:
        msg_id = msg.get("id")
        if msg_id in seen_ids:
            continue
        title, body = parse_message(msg)
        create_task_for_message(title, body)
        seen_ids.add(msg_id)
        created += 1

    state["seen_ids"] = list(seen_ids)
    save_state(state)
    print(f"Created {created} new task(s) in Vault/Needs_Action.")


if __name__ == "__main__":
    main()
