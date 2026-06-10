"""Purpose: Groq API clients with live and mock execution modes for demo-safe middleware."""

from __future__ import annotations

from datetime import date
from decimal import Decimal
import json
import logging
import os
import re
import time
from typing import Any

from groq import APIError, Groq, RateLimitError

LOGGER = logging.getLogger(__name__)
DEFAULT_MODEL = "llama3-8b-8192"


class AIClientError(RuntimeError):
    """Raised when the AI client cannot satisfy a request."""


class BaseAIClient:
    """Base interface shared by live and mock AI clients."""

    mode = "unknown"

    def analyze_lead(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Analyze a lead payload."""

        raise NotImplementedError

    def extract_invoice(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Extract structured data from invoice text."""

        raise NotImplementedError

    def generate_message(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Generate a WhatsApp-ready business reply."""

        raise NotImplementedError


class GroqJSONClient(BaseAIClient):
    """Small wrapper around the Groq client for JSON-first responses."""

    mode = "live"

    def __init__(self, api_key: str | None = None, model: str = DEFAULT_MODEL) -> None:
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise AIClientError("GROQ_API_KEY is required for live AI mode.")
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
        raise AIClientError(f"Groq request failed after retries: {last_error}") from last_error

    def analyze_lead(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Analyze CRM lead data with the configured Groq model."""

        system_prompt = (
            "You are a CRM lead qualification assistant. "
            "Return JSON with keys score, summary, next_action, priority. "
            "Priority must be one of low, medium, high, urgent."
        )
        user_prompt = (
            "Analyze this lead for ERP, backend automation, and Odoo implementation services:\n"
            f"{json.dumps(payload, indent=2)}"
        )
        return self.complete_json(system_prompt, user_prompt)

    def extract_invoice(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Extract vendor bill data from raw invoice text."""

        system_prompt = (
            "You extract structured accounts payable data. "
            "Return JSON with vendor, amount, date, line_items, currency. "
            "Each line item needs description, quantity, unit_price, total."
        )
        user_prompt = f"Extract invoice data from this text:\n{payload['raw_text']}"
        return self.complete_json(system_prompt, user_prompt)

    def generate_message(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Generate a structured customer message."""

        system_prompt = (
            "You write concise, helpful WhatsApp business replies. "
            "Return JSON with message, tone, suggested_actions. "
            "Tone must be one of friendly, professional, empathetic, urgent."
        )
        user_prompt = f"Create a message for the following context:\n{json.dumps(payload, indent=2)}"
        return self.complete_json(system_prompt, user_prompt)


class MockGroqJSONClient(BaseAIClient):
    """Deterministic mock client used for local demos when no live API key is available."""

    mode = "mock"

    @staticmethod
    def _usage() -> dict[str, Any]:
        """Return synthetic usage metadata for mock responses."""

        return {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0, "model": "mock-heuristic"}

    def analyze_lead(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Generate a simple deterministic lead qualification response."""

        score = 4
        if payload.get("email"):
            score += 1
        if payload.get("phone"):
            score += 1
        if payload.get("company"):
            score += 1
        if len(payload.get("description", "")) > 80:
            score += 2
        if any(keyword in payload.get("description", "").lower() for keyword in ("urgent", "migration", "automation", "odoo")):
            score += 1
        score = min(score, 10)
        priority = "urgent" if score >= 9 else "high" if score >= 7 else "medium" if score >= 5 else "low"
        response = {
            "score": score,
            "summary": (
                "Mock mode lead analysis: this prospect appears suitable for an Odoo and automation discovery workflow."
            ),
            "next_action": "Schedule a short discovery call and capture current ERP process pain points.",
            "priority": priority,
            "_usage": self._usage(),
        }
        return response

    def extract_invoice(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Extract invoice fields using lightweight pattern matching."""

        raw_text = payload.get("raw_text", "")
        vendor_match = re.search(r"vendor[:\s]+(.+)", raw_text, flags=re.IGNORECASE)
        amount_match = re.search(r"(total|amount)[:\s]+([0-9]+(?:\.[0-9]{1,2})?)", raw_text, flags=re.IGNORECASE)
        currency_match = re.search(r"\b(USD|EUR|GBP|PKR|AED|SAR)\b", raw_text)
        date_match = re.search(r"\b(\d{4}-\d{2}-\d{2})\b", raw_text)
        line_total = Decimal(amount_match.group(2)) if amount_match else Decimal("0")
        response = {
            "vendor": vendor_match.group(1).strip() if vendor_match else "Demo Vendor",
            "amount": line_total,
            "date": date.fromisoformat(date_match.group(1)) if date_match else date.today(),
            "line_items": [
                {
                    "description": "Imported invoice line",
                    "quantity": 1,
                    "unit_price": line_total,
                    "total": line_total,
                }
            ],
            "currency": currency_match.group(1) if currency_match else "USD",
            "_usage": self._usage(),
        }
        return response

    def generate_message(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Return a deterministic demo-friendly WhatsApp message."""

        customer_name = payload.get("customer_name", "there")
        intent = payload.get("intent", "follow_up").replace("_", " ")
        response = {
            "message": (
                f"Hi {customer_name}, thanks for reaching out. This is a mock-mode response for {intent}. "
                "A consultant can review your request and follow up shortly."
            ),
            "tone": "professional",
            "suggested_actions": [
                "Log the interaction in Odoo",
                "Schedule a discovery follow-up",
            ],
            "_usage": self._usage(),
        }
        return response


def get_ai_client() -> BaseAIClient:
    """Return either a live Groq client or a local mock client depending on environment."""

    force_mock = os.getenv("AI_MOCK_MODE", "false").lower() == "true"
    if force_mock or not os.getenv("GROQ_API_KEY"):
        LOGGER.info("Using mock AI mode for middleware responses.")
        return MockGroqJSONClient()
    return GroqJSONClient(model=os.getenv("GROQ_MODEL", DEFAULT_MODEL))
