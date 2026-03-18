"""Skill: Process tasks from the vault.

This skill implements the full workflow:
1. Read tasks from Vault/Needs_Action
2. Generate/overwrite Vault/Plans/Plan.md
3. Check if approval is required (moves those tasks to Vault/Pending_Approval)
4. If approved, execute actions
5. Move processed tasks to Vault/Done

This is the canonical "process tasks" handler used by the service.
"""

from __future__ import annotations

from src.claude_agent import process_tasks


def run() -> None:
    """Run the full task processing pipeline."""
    process_tasks()
