from pathlib import Path
import re
import json
import requests
from typing import Dict, Any

BASE_DIR = Path(__file__).resolve().parents[1]
VAULT = BASE_DIR / "Vault"


def execute_mcp_action(action_data: Dict[str, Any]) -> bool:
    """Execute action via MCP server."""
    action = action_data.get("action")
    if action == "send_email":
        url = "http://localhost:3000/send-email"
        resp = requests.post(url, json=action_data.get("params", {}), timeout=30)
        resp.raise_for_status()
        print(f"MCP send_email success: {resp.json()}")
        return True
    elif action == "linkedin_post":
        url = "http://localhost:3000/linkedin-post"
        resp = requests.post(url, json=action_data.get("params", {}), timeout=120)
        resp.raise_for_status()
        print(f"MCP linkedin_post success: {resp.json()}")
        return True
    elif action == "run_action":
        url = "http://localhost:3000/run-action"
        resp = requests.post(url, json=action_data.get("params", {}), timeout=120)
        resp.raise_for_status()
        print(f"MCP run_action success: {resp.json()}")
        return True
    else:
        print(f"Unknown action: {action}")
        return False


def process_approved() -> None:
    approved = VAULT / "Approved"
    done = VAULT / "Done"
    done.mkdir(parents=True, exist_ok=True)

    for file_path in approved.glob("*.md"):
        print(f"Processing approved task: {file_path.name}")
        content = file_path.read_text(encoding="utf-8")
        
        # Extract JSON block
        json_match = re.search(r"```json\s*(\{.*?\})\s*```", content, re.DOTALL)
        if json_match:
            try:
                action_json = json.loads(json_match.group(1))
                print(f"Executing action: {action_json}")
                if execute_mcp_action(action_json):
                    print("Action executed successfully.")
                else:
                    print("Action failed.")
            except json.JSONDecodeError as e:
                print(f"Invalid JSON in {file_path.name}: {e}")
        else:
            print(f"No JSON action block found in {file_path.name}")
        
        # Move to Done
        file_path.rename(done / file_path.name)


if __name__ == "__main__":
    process_approved()
