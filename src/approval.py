"""Human-in-the-loop approval helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.utils.vault import normalize_filename, task_header, write_task, list_tasks, move_task, vault_path
from src.skills.email_skill import send_email
from src.skills.linkedin_skill import post_linkedin
from src.skills.mcp_skill import run_mcp_action


def create_approval_request(action: str, params: dict[str, Any], reason: str | None = None) -> Path:
    """Create a pending approval markdown file for a sensitive action."""
    title = f"Approval request: {action}"
    payload = {"action": action, "params": params}
    if reason:
        payload["reason"] = reason

    body = """Please review the following action and move this file to `Approved/` to execute.

```json
""" + json.dumps(payload, indent=2) + "\n```\n"

    filename = normalize_filename(f"approval_{action}_{params.get('to', params.get('target', ''))}")
    return write_task("Pending_Approval", filename, task_header(title) + body)


def execute_approved_actions() -> None:
    """Execute approved actions in the vault."""
    approved = list_tasks("Approved")
    for task in approved:
        content = task.read_text(encoding="utf-8")
        try:
            json_start = content.index("```json")
            json_end = content.index("```", json_start + 1)
            json_text = content[json_start + len("```json"):json_end].strip()
            payload = json.loads(json_text)
        except Exception as e:
            print(f"Skipping {task.name}: cannot parse json payload ({e})")
            continue

        action = payload.get("action")
        params = payload.get("params", {})
        print(f"Executing approved action {action} from {task.name}")
        try:
            if action == "send_email":
                send_email(
                    to=params["to"],
                    subject=params.get("subject", ""),
                    text=params.get("text", ""),
                    html=params.get("html"),
                )
            elif action == "post_linkedin":
                post_linkedin(params.get("content", ""))
            elif action == "run_mcp":
                run_mcp_action(params.get("command", ""))
            else:
                print(f"Unknown action: {action}")
                continue
            move_task(task, "Done")
            print(f"Completed {task.name}")
        except Exception as e:
            print(f"Failed to execute {task.name}: {e}")
