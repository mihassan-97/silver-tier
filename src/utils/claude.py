"""Helpers for talking to Claude (Anthropic)."""

from typing import Optional

from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

from src.config import settings


def get_anthropic_client() -> Anthropic:
    return Anthropic(api_key=settings.CLAUDE_API_KEY)


def claude_complete(
    prompt: str,
    model: Optional[str] = None,
    max_tokens_to_sample: int = 1000,
    temperature: float = 0.7,
) -> str:
    """Call Claude to complete the given prompt."""
    client = get_anthropic_client()
    model = model or settings.CLAUDE_MODEL
    response = client.completions.create(
        model=model,
        prompt=f"{HUMAN_PROMPT}{prompt}{AI_PROMPT}",
        max_tokens_to_sample=max_tokens_to_sample,
        temperature=temperature,
    )
    return response.completion
