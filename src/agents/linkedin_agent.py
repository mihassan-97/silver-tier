from pathlib import Path
from datetime import datetime

VAULT = Path("Vault")


def generate_post():
    return f"""---
type: linkedin_post
date: {datetime.now().isoformat()}
status: pending
---

🚀 Our AI Employee is helping automate business workflows!

#AI #Automation #Startup
"""


def create_linkedin_task():
    file_path = VAULT / "Needs_Action" / f"LINKEDIN_{datetime.now().timestamp()}.md"
    file_path.write_text(generate_post(), encoding="utf-8")
    print("LinkedIn task created:", file_path)


if __name__ == "__main__":
    create_linkedin_task()
