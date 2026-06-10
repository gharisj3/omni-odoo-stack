"""Purpose: Run a small smoke test against the FastAPI middleware endpoints."""

from __future__ import annotations

import argparse
import json
import os
import urllib.error
import urllib.request


def call_json(url: str, method: str = "GET", headers: dict[str, str] | None = None, payload: dict | None = None) -> dict:
    """Send an HTTP request and decode the JSON response."""

    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(url=url, method=method, data=data, headers=headers or {})
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> int:
    """Execute health and lead-analysis smoke tests."""

    parser = argparse.ArgumentParser(description="Smoke test the omni-odoo-stack AI middleware.")
    parser.add_argument("--base-url", default="http://localhost:8000", help="Base URL for the middleware.")
    args = parser.parse_args()

    api_key = os.getenv("AI_SHARED_API_KEY", "replace_with_shared_fastapi_key")
    headers = {"X-API-Key": api_key, "Content-Type": "application/json"}

    try:
        health = call_json(f"{args.base_url}/health")
        print("Health:", json.dumps(health))

        lead_payload = {
            "name": "Smoke Test Prospect",
            "email": "ops@example.com",
            "phone": "+923001234567",
            "description": "Need Odoo CRM, AI middleware, and n8n workflow automation support.",
            "company": "Smoke Test Co",
        }
        result = call_json(f"{args.base_url}/analyze/lead", method="POST", headers=headers, payload=lead_payload)
        print("Analyze lead:", json.dumps(result))
        return 0
    except urllib.error.HTTPError as exc:
        print(f"HTTP error: {exc.code} {exc.reason}")
        print(exc.read().decode("utf-8"))
        return 1
    except urllib.error.URLError as exc:
        print(f"Connection error: {exc.reason}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
