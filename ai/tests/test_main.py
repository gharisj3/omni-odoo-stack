"""Purpose: Lightweight endpoint tests for the FastAPI middleware in mock mode."""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

from fastapi.testclient import TestClient

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def build_client(monkeypatch) -> TestClient:
    """Build a TestClient with mock mode enabled for deterministic tests."""

    monkeypatch.setenv("AI_SHARED_API_KEY", "test-key")
    monkeypatch.setenv("AI_MOCK_MODE", "true")
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    module = importlib.import_module("ai.middleware.main")
    module = importlib.reload(module)
    return TestClient(module.app)


def auth_headers() -> dict[str, str]:
    """Return shared request headers used in endpoint tests."""

    return {"X-API-Key": "test-key"}


def test_health_endpoint_reports_mock_mode(monkeypatch) -> None:
    """Health endpoint should confirm mock mode when no Groq key exists."""

    client = build_client(monkeypatch)
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["mode"] == "mock"


def test_auth_is_required(monkeypatch) -> None:
    """Protected endpoints should reject missing API keys."""

    client = build_client(monkeypatch)
    response = client.post("/analyze/lead", json={})
    assert response.status_code == 401


def test_analyze_lead_returns_structured_response(monkeypatch) -> None:
    """Lead analysis should return a valid structured payload."""

    client = build_client(monkeypatch)
    response = client.post(
        "/analyze/lead",
        headers=auth_headers(),
        json={
            "name": "Demo Prospect",
            "email": "ops@example.com",
            "phone": "+923001234567",
            "description": "Need Odoo, CRM, and backend automation discovery support.",
            "company": "Demo Co",
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["mode"] == "mock"
    assert 1 <= payload["result"]["score"] <= 10


def test_extract_invoice_returns_envelope(monkeypatch) -> None:
    """Invoice extraction should return deterministic demo output."""

    client = build_client(monkeypatch)
    response = client.post(
        "/extract/invoice",
        headers=auth_headers(),
        json={"raw_text": "Vendor: Atlas Supplies\nDate: 2026-06-01\nTotal: 1550 USD\n1 x Steel Shelving 1550"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["result"]["vendor"] == "Atlas Supplies"
    assert payload["result"]["currency"] == "USD"


def test_generate_message_returns_business_reply(monkeypatch) -> None:
    """Message generation should return a usable WhatsApp reply."""

    client = build_client(monkeypatch)
    response = client.post(
        "/generate/message",
        headers=auth_headers(),
        json={
            "context": "A client wants to know when a project quote will be ready.",
            "customer_name": "Ayesha",
            "intent": "quote_follow_up",
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert "Ayesha" in payload["result"]["message"]
    assert payload["result"]["tone"] == "professional"
