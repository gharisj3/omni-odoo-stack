"""Purpose: FastAPI service that exposes lead analysis, invoice extraction, and message generation endpoints."""

from __future__ import annotations

import json
import logging
import os
from typing import Annotated, Any

from fastapi import Depends, FastAPI, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from middleware.groq_client import GroqJSONClient
from middleware.validators import (
    InvoiceData,
    InvoiceInput,
    LeadAnalysis,
    LeadInput,
    MessageInput,
    MessageOutput,
)

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

APP_NAME = "omni-odoo-stack-ai"
API_KEY_HEADER = "X-API-Key"

app = FastAPI(title=APP_NAME, version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def require_api_key(x_api_key: Annotated[str | None, Header(alias=API_KEY_HEADER)] = None) -> None:
    """Validate shared API access for all private middleware endpoints."""

    expected_key = os.getenv("AI_SHARED_API_KEY")
    if not expected_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="AI_SHARED_API_KEY is not configured.",
        )
    if x_api_key != expected_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key.")


def get_groq_client() -> GroqJSONClient:
    """Create a Groq client instance for the current request."""

    return GroqJSONClient()


@app.get("/health")
def health() -> dict[str, str]:
    """Return a basic health response for uptime checks."""

    return {"status": "ok", "service": APP_NAME}


@app.post("/analyze/lead", response_model=LeadAnalysis, dependencies=[Depends(require_api_key)])
def analyze_lead(payload: LeadInput) -> LeadAnalysis:
    """Analyze a CRM lead and return a structured priority and next-step recommendation."""

    client = get_groq_client()
    system_prompt = (
        "You are a CRM lead qualification assistant. "
        "Return JSON with keys score, summary, next_action, priority. "
        "Priority must be one of low, medium, high, urgent."
    )
    user_prompt = (
        "Analyze this lead for ERP and automation services:\n"
        f"{payload.model_dump_json(indent=2)}"
    )
    response = client.complete_json(system_prompt, user_prompt)
    usage = response.pop("_usage", {})
    LOGGER.info("Lead analysis token usage: %s", json.dumps(usage))
    return LeadAnalysis.model_validate(response)


@app.post("/extract/invoice", response_model=InvoiceData, dependencies=[Depends(require_api_key)])
def extract_invoice(payload: InvoiceInput) -> InvoiceData:
    """Extract structured vendor bill data from unstructured invoice text."""

    client = get_groq_client()
    system_prompt = (
        "You extract structured accounts payable data. "
        "Return JSON with vendor, amount, date, line_items, currency. "
        "Each line item needs description, quantity, unit_price, total."
    )
    user_prompt = f"Extract invoice data from this text:\n{payload.raw_text}"
    response = client.complete_json(system_prompt, user_prompt)
    usage = response.pop("_usage", {})
    LOGGER.info("Invoice extraction token usage: %s", json.dumps(usage))
    return InvoiceData.model_validate(response)


@app.post("/generate/message", response_model=MessageOutput, dependencies=[Depends(require_api_key)])
def generate_message(payload: MessageInput) -> MessageOutput:
    """Generate a WhatsApp-ready customer reply and suggested internal next actions."""

    client = get_groq_client()
    system_prompt = (
        "You write concise, helpful WhatsApp business replies. "
        "Return JSON with message, tone, suggested_actions. "
        "Tone must be one of friendly, professional, empathetic, urgent."
    )
    user_prompt = (
        "Create a message for the following context:\n"
        f"{payload.model_dump_json(indent=2)}"
    )
    response = client.complete_json(system_prompt, user_prompt)
    usage = response.pop("_usage", {})
    LOGGER.info("Message generation token usage: %s", json.dumps(usage))
    return MessageOutput.model_validate(response)
