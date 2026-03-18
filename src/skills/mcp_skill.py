"""MCP integration skill."""

from __future__ import annotations

import requests


def run_mcp_action(command: str) -> dict:
    """Run an arbitrary action via the MCP server."""
    url = "http://localhost:3000/run-action"
    resp = requests.post(url, json={"command": command}, timeout=120)
    resp.raise_for_status()
    return resp.json()
