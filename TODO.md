# Silver Tier AI Employee Setup & Fix 404 Error

## Done (from previous)
- [x] MCP server basics fixed
- [x] Python deps migrated
- [x] Tests pass

## Implementation Steps (Approved Plan)
1. [x] Create config.env with placeholders for CLAUDE_API_KEY, SMTP creds (copy to .env)
2. [x] Update src/approval_executor.py to parse/execute JSON actions via MCP
3. [x] Create sample Vault/Needs_Action/test_task.md
4. [ ] Test: Fill .env with real CLAUDE_API_KEY + SMTP, `cd mcp_server && npm install && node server.js`, `python -m pip install -r requirements.txt`, `python src/claude_agent.py`
5. [ ] Test approval: Move Vault/Pending_Approval/email.md -> Vault/Approved/, `python src/approval_executor.py`

**Setup complete! Copy config.env -> .env, fill secrets, and run tests.**
