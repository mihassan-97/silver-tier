# Silver Tier Personal AI Employee

## Overview
This project implements a **local-first Personal AI Employee** using:

- **Obsidian-style vault** (local Markdown files) for memory & dashboard
- **Claude Code** (Anthropic) as the reasoning agent
- **Python watchers** for perception (Gmail + file system)
- **MCP server** for actions (email sending / browser automation)
- **Human-in-the-loop approvals** via vault folders

---

## Folder Structure
- `Vault/` - Obsidian-style vault for storing notes and tasks
  - `Inbox/` - Incoming raw inputs
  - `Needs_Action/` - Tasks that need processing
  - `Plans/` - Generated plan files (e.g., `Plan.md`)
  - `Done/` - Completed tasks
  - `Pending_Approval/` - Awaiting human approval for sensitive actions
  - `Approved/` - Approved actions
  - `Rejected/` - Rejected actions
  - `Dashboard.md` - High-level status & links
  - `Company_Handbook.md` - Your policies & guidelines

## Getting Started
1. **Install dependencies**
   - Python: `python -m pip install -r requirements.txt`
   - Node: `npm install` (run inside `mcp_server/`)

2. **Create `.env`**
   - Copy `.env.example` to `.env` and fill secrets.

3. **Initialize Gmail API (optional)**
   - Follow instructions in `src/watchers/gmail_watcher.py` to create OAuth credentials.

4. **Run watchers**
   - `python -m src.watchers.gmail_watcher` (or run `python src/watchers/gmail_watcher.py`)
   - `python -m src.watchers.fs_watcher`

5. **Run the Claude processor**
   - `python -m src.claude_agent` (or `python src/claude_agent.py`)

6. **Start MCP server**
   - `node mcp_server/server.js`

---

## How It Works
1. **Watchers** detect new events and create Markdown tasks in `Vault/Needs_Action`
2. **Claude Agent** reads `Needs_Action`, generates a plan (`Vault/Plans/Plan.md`), and moves completed tasks to `Vault/Done`

   - If the plan includes a JSON action block like `send_email`, the system will call the MCP server to send the email automatically.

3. **Human-in-the-loop (HITL)**

   - Sensitive actions (email, payments, etc.) are written as task files into `Vault/Pending_Approval`.
   - A human must manually move the file from `Vault/Pending_Approval` → `Vault/Approved` to authorize execution.
   - Once approved, run `python -m src.approval_executor` to execute the approved actions.

4. **MCP Server** executes actions (email sending / browser automation) when instructed

---

## LinkedIn Automation
- Generates business posts automatically
- Saves posts in `/Needs_Action` (via `src/agents/linkedin_agent.py`)
- Can be extended to auto-post via Playwright or LinkedIn API

---

## Scheduling
On Windows, use Task Scheduler to run:
- `python -m src.claude_agent` daily
- `python -m src.scheduler weekly_summary` weekly

---

## Notes
- **Secrets must not be stored in the Vault**.
- All credentials are managed via `.env` and (optionally) local OS credential stores.
