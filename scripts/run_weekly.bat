@echo off
REM Run weekly summary generation.
echo Generating weekly summary...
python -m src.scheduler weekly
echo Weekly summary complete.
