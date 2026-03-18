def generate_post() -> str:
    return "🚀 AI Employee helping automate business!"


def save_post(vault: str) -> None:
    with open(vault + "/Needs_Action/linkedin_post.md", "w", encoding="utf-8") as f:
        f.write(generate_post())
