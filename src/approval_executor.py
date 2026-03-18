from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
VAULT = BASE_DIR / "Vault"


def process_approved() -> None:
    approved = VAULT / "Approved"
    done = VAULT / "Done"
    done.mkdir(parents=True, exist_ok=True)

    for file in approved.glob("*.md"):
        print("Executing approved task:", file.name)
        file.rename(done / file.name)


if __name__ == "__main__":
    process_approved()
