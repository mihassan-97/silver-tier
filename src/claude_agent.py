"""Claude agent for processing tasks and generating plans."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

from src.skills.email_skill import send_email
from src.utils.claude import claude_complete
from src.utils.vault import (
    ensure_vault_structure,
    list_tasks,
    move_task,
    task_header,
    timestamp,
    vault_path,
)
from src.approval_filter import filter_tasks_for_approval


def build_prompt(tasks: list[Path]) -> str:
    if not tasks:
        return "You are a personal AI assistant. There are no tasks to process."

    tasks_text = []
    for t in tasks:
        tasks_text.append(f"---\n{t.read_text(encoding='utf-8')}\n")

    prompt = (
        "You are a personal AI employee managing an Obsidian vault. "
        "A set of tasks has been placed into Vault/Needs_Action. "
        "For each task, provide a short plan with steps, prioritize items, and identify any sensitive actions that require human approval. "
        "Output a Markdown plan with headers and actionable steps. "
        "Also, if a task can be marked as completed, include a section 'Completed Tasks' listing the filenames.\n\n"
        "If you want to trigger an automated action (like sending an email), include a JSON action block in the plan, e.g.:\n````json\n{\n  \"action\": \"send_email\",\n  \"params\": {\n    \"to\": \"example@domain.com\",\n    \"subject\": \"Hello\",\n    \"text\": \"Body\"\n  }\n}\n````\n\n"
        "Here are the tasks:\n"
        + "\n".join(tasks_text)
        + "\nPlease produce a clear plan in Markdown." 
    )
    return prompt


def write_plan(plan_text: str) -> Path:
    ensure_vault_structure()
    plan_path = vault_path("Plans", "Plan.md")
    content = task_header("Plan", {"generated": timestamp()}) + plan_text.strip() + "\n"
    plan_path.write_text(content, encoding="utf-8")
    return plan_path


def create_plan(task_file: Path) -> Path:
    """Create a lightweight plan file for a given task."""
    ensure_vault_structure()
    plan_path = vault_path("Plans", f"PLAN_{task_file.stem}.md")
    content = f"""# Plan for {task_file.name}\n\n- [x] Read task\n- [ ] Analyze request\n- [ ] Decide action\n- [ ] Execute task\n- [ ] Move to Done\n"""
    plan_path.write_text(content, encoding="utf-8")
    return plan_path


def execute_actions_from_plan(plan_text: str) -> None:
    """Look for JSON action blocks in the plan and execute known actions."""
    # Find blocks like ```json ... ```
    matches = re.findall(r"```json\s*(\{.*?\})\s*```", plan_text, flags=re.DOTALL)
    for match in matches:
        try:
            payload = json.loads(match)
        except Exception as exc:
            print(f"Skipping invalid JSON action block: {exc}")
            continue

        action = payload.get("action")
        params = payload.get("params", {})

        if action == "send_email":
            try:
                send_email(
                    to=params.get("to", ""),
                    subject=params.get("subject", ""),
                    text=params.get("text", ""),
                    html=params.get("html"),
                )
                print(f"Sent email to {params.get('to')}")
            except Exception as e:
                print(f"Failed to send email: {e}")
        else:
            print(f"Unknown action in plan: {action}")


def process_tasks() -> None:
    ensure_vault_structure()
    tasks = list_tasks("Needs_Action")
    if not tasks:
        print("No tasks in Vault/Needs_Action.")
        return

    tasks = filter_tasks_for_approval(tasks)
    if not tasks:
        print("All tasks were moved to Pending_Approval.")
        return

    prompt = build_prompt(tasks)
    print(f"Calling Claude with {len(tasks)} task(s)...")
    plan = claude_complete(prompt)
    print("Claude response received. Writing plan...")
    write_plan(plan)

    # Execute any actions embedded in the plan (e.g., send email)
    execute_actions_from_plan(plan)

    # Move tasks to Done after processing to avoid duplicate work.
    for task in tasks:
        move_task(task, "Done")

    print(f"Moved {len(tasks)} task(s) to Vault/Done.")


if __name__ == "__main__":
    process_tasks()
