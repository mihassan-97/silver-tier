"""Claude Agent Skills for the Personal AI Employee.

Skills are small Python helpers that can be called from the agent logic.
The intent is to make it straightforward for the agent to read tasks, create drafts,
request approvals, and invoke actions via the MCP server.
"""

from .task_skill import (
    approve_task,
    complete_task,
    list_needs_action,
    read_task,
    reject_task,
    require_approval,
)
from .email_skill import create_email_task, send_email
from .linkedin_skill import create_linkedin_draft, post_linkedin
from .mcp_skill import run_mcp_action

__all__ = [
    "approve_task",
    "complete_task",
    "list_needs_action",
    "read_task",
    "reject_task",
    "require_approval",
    "create_email_task",
    "send_email",
    "create_linkedin_draft",
    "post_linkedin",
    "run_mcp_action",
]
