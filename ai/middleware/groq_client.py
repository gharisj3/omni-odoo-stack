"""Purpose: Groq API client with retries, structured outputs, and token tracking."""

from __future__ import annotations

import json
import logging
import os
import time
from typing import Any

from groq import APIError, Groq, RateLimitError

LOGGER = logging.getLogger(__name__)
DEFAULT_MODEL = "llama3-8b-8192"


class GroqJSONClient:
    """Small wrapper around the Groq client for JSON-first responses."""

    def __init__(self, api_key: str | None = None, model: str = DEFAULT_MODEL) -> None:
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise RuntimeError("GROQ_API_KEY is required to start the AI middleware.")
        self.model = model
        self.client = Groq(api_key=self.api_key)

    def complete_json(self, system_prompt: str, user_prompt: str) -> dict[str, Any]:
        """Execute a chat completion and force a JSON object response."""

        last_error: Exception | None = None
        for attempt in range(1, 4):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    temperature=0.2,
                    response_format={"type": "json_object"},
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                )
                content = response.choices[0].message.content or "{}"
                usage = getattr(response, "usage", None)
                payload = json.loads(content)
                payload["_usage"] = {
                    "prompt_tokens": getattr(usage, "prompt_tokens", 0),
                    "completion_tokens": getattr(usage, "completion_tokens", 0),
                    "total_tokens": getattr(usage, "total_tokens", 0),
                    "model": self.model,
                }
                return payload
            except (RateLimitError, APIError, json.JSONDecodeError) as exc:
                last_error = exc
                backoff = 2 ** (attempt - 1)
                LOGGER.warning("Groq request failed on attempt %s: %s", attempt, exc)
                time.sleep(backoff)
        raise RuntimeError(f"Groq request failed after retries: {last_error}") from last_error

