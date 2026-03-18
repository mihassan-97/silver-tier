@echo off
REM Run daily processing (claude agent) and approval runner.

echo Running daily processing...
python -m src.claude_agent

echo Running approved action executor...
python -m src.approval_runner

echo Daily run complete.
