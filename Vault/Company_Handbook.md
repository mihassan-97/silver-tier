# Company Handbook

## Purpose
This handbook describes the policies, guidelines, and operating procedures for the Personal AI Employee.

## Core Principles
- **Local-first**: Keep all memory and state local.
- **Human-in-the-loop**: Sensitive actions require explicit human approval.
- **Transparency**: All tasks and plans are stored as Markdown in the vault.

## Security
- Store secrets in `.env` only.
- Never commit `.env` or credential files.

## Workflows
### Task ingestion
- New items are added to `Vault/Needs_Action` by watchers.

### Planning
- Run `python -m src.claude_agent` to generate `Vault/Plans/Plan.md`.

### Execution
- Approved actions are moved to `Vault/Approved`.
- MCP server executes after approval.
