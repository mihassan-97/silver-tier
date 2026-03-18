# Process Task Skill

This skill orchestrates the full workflow for processing tasks from the vault:

1. Read tasks from `Vault/Needs_Action`
2. Generate `Vault/Plans/Plan.md` via Claude
3. Check if approval is required (moves those tasks to `Vault/Pending_Approval`)
4. If no approval is needed, execute actions (e.g., send email)
5. Move processed tasks to `Vault/Done`

## Usage

```python
from src.skills.process_task import run

run()
```
