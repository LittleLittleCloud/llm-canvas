"""Utility functions for examples."""

from __future__ import annotations

import re
from typing import Union

from anthropic import Anthropic
from anthropic.types import MessageParam

from llm_canvas.types import Message


def llm_call(prompt: Union[str, Message], system_prompt: str = "", model: str = "claude-3-5-sonnet-20241022") -> str:
    """
    Calls the model with the given prompt and returns the response.

    Args:
        prompt (Union[str, Message]): The user prompt to send to the model.
                                     Can be a simple string or a Message object with rich content.
        system_prompt (str, optional): The system prompt to send to the model. Defaults to "".
        model (str, optional): The model to use for the call. Defaults to "claude-3-5-sonnet-20241022".

    Returns:
        str: The response from the language model.
    """
    client = Anthropic()

    # Handle both string and Message inputs
    user_message: Union[MessageParam, None] = (
        {"role": "user", "content": prompt}
        if isinstance(prompt, str)
        else MessageParam(role=prompt["role"], content=prompt["content"])
        if prompt["role"] != "system"
        else None
    )

    if user_message is None:
        raise TypeError("Invalid prompt type. Must be str or Message and role can't be system.")

    response = client.messages.create(
        model=model,
        max_tokens=4096,
        system=system_prompt,
        messages=[user_message],  # type: ignore[arg-type]
        temperature=0.1,
    )

    # Extract text from the first content block
    content_block = response.content[0]
    if hasattr(content_block, "text"):
        return content_block.text
    # Fallback for non-text blocks
    return str(content_block)


def extract_xml(text: str, tag: str) -> str:
    """
    Extracts the content of the specified XML tag from the given text. Used for parsing structured responses

    Args:
        text (str): The text containing the XML.
        tag (str): The XML tag to extract content from.

    Returns:
        str: The content of the specified XML tag, or an empty string if the tag is not found.
    """
    match = re.search(f"<{tag}>(.*?)</{tag}>", text, re.DOTALL)
    return match.group(1) if match else ""
