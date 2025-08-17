"""Utility functions for examples."""

from __future__ import annotations

from anthropic import Anthropic


def llm_call(prompt: str, system_prompt: str = "", model: str = "claude-3-5-sonnet-20241022") -> str:
    """
    Calls the model with the given prompt and returns the response.

    Args:
        prompt (str): The user prompt to send to the model.
        system_prompt (str, optional): The system prompt to send to the model. Defaults to "".
        model (str, optional): The model to use for the call. Defaults to "claude-3-5-sonnet-20241022".

    Returns:
        str: The response from the language model.
    """
    client = Anthropic()
    response = client.messages.create(
        model=model,
        max_tokens=4096,
        system=system_prompt,
        messages=[{"role": "user", "content": prompt}],  # type: ignore[arg-type]
        temperature=0.1,
    )

    # Extract text from the first content block
    content_block = response.content[0]
    if hasattr(content_block, "text"):
        return content_block.text
    # Fallback for non-text blocks
    return str(content_block)
