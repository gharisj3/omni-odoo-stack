"""Purpose: FastAPI service that exposes lead analysis, invoice extraction, and message generation endpoints."""

from __future__ import annotations

import json
import logging
import os
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

try:
    from middleware.groq_client import AIClientError, get_ai_client
    from middleware.validators import (
        ErrorResponse,
        HealthResponse,
        InvoiceExtractionEnvelope,
        InvoiceInput,
        LeadAnalysisEnvelope,
        LeadInput,
        MessageGenerationEnvelope,
        MessageInput,
    )
except ImportError:  # pragma: no cover - used for local package execution
    from ai.middleware.groq_client import AIClientError, get_ai_client
    from ai.middleware.validators import (
        ErrorResponse,
        HealthResponse,
        InvoiceExtractionEnvelope,
        InvoiceInput,
        LeadAnalysisEnvelope,
        LeadInput,
        MessageGenerationEnvelope,
        MessageInput,
    )

logging.basicConfig(level=os.getenv("AI_LOG_LEVEL", "INFO"))
LOGGER = logging.getLogger(__name__)

APP_NAME = "omni-odoo-stack-ai"
API_KEY_HEADER = "X-API-Key"

app = FastAPI(
    title=APP_NAME,
    version="1.1.0",
    description="Production-style portfolio middleware for ERP AI enrichment and demo-safe mock execution.",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("AI_CORS_ORIGINS", "*").split(","),
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Return a concise error payload and log validation failures."""

    LOGGER.warning("Validation error on %s: %s", request.url.path, exc.errors())
    return JSONResponse(status_code=422, content={"detail": "Invalid request payload.", "errors": exc.errors()})


@app.exception_handler(AIClientError)
async def ai_client_exception_handler(request: Request, exc: AIClientError) -> JSONResponse:
    """Convert AI client failures into consistent HTTP errors."""

    LOGGER.error("AI client error on %s: %s", request.url.path, exc)
    return JSONResponse(status_code=502, content={"detail": str(exc)})


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch unexpected exceptions so the API always returns JSON."""

    LOGGER.exception("Unhandled middleware error on %s", request.url.path)
    return JSONResponse(status_code=500, content={"detail": "Unexpected server error."})


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


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Return a basic health response for uptime checks."""

    client = get_ai_client()
    return HealthResponse(
        status="ok",
        service=APP_NAME,
        mode=client.mode,
        groq_configured=bool(os.getenv("GROQ_API_KEY")),
    )


@app.post(
    "/analyze/lead",
    response_model=LeadAnalysisEnvelope,
    responses={401: {"model": ErrorResponse}, 422: {"model": ErrorResponse}, 502: {"model": ErrorResponse}},
    dependencies=[Depends(require_api_key)],
)
def analyze_lead(payload: LeadInput) -> LeadAnalysisEnvelope:
    """Analyze a CRM lead and return a structured priority and next-step recommendation."""

    client = get_ai_client()
    response = client.analyze_lead(payload.model_dump())
    usage = response.pop("_usage", {})
    LOGGER.info("Lead analysis completed in %s mode with usage %s", client.mode, json.dumps(usage))
    return LeadAnalysisEnvelope(result=response, mode=client.mode)


@app.post(
    "/extract/invoice",
    response_model=InvoiceExtractionEnvelope,
    responses={401: {"model": ErrorResponse}, 422: {"model": ErrorResponse}, 502: {"model": ErrorResponse}},
    dependencies=[Depends(require_api_key)],
)
def extract_invoice(payload: InvoiceInput) -> InvoiceExtractionEnvelope:
    """Extract structured vendor bill data from unstructured invoice text."""

    client = get_ai_client()
    response = client.extract_invoice(payload.model_dump())
    usage = response.pop("_usage", {})
    LOGGER.info("Invoice extraction completed in %s mode with usage %s", client.mode, json.dumps(usage))
    return InvoiceExtractionEnvelope(result=response, mode=client.mode)


@app.post(
    "/generate/message",
    response_model=MessageGenerationEnvelope,
    responses={401: {"model": ErrorResponse}, 422: {"model": ErrorResponse}, 502: {"model": ErrorResponse}},
    dependencies=[Depends(require_api_key)],
)
def generate_message(payload: MessageInput) -> MessageGenerationEnvelope:
    """Generate a WhatsApp-ready customer reply and suggested internal next actions."""

    client = get_ai_client()
    response = client.generate_message(payload.model_dump())
    usage = response.pop("_usage", {})
    LOGGER.info("Message generation completed in %s mode with usage %s", client.mode, json.dumps(usage))
    return MessageGenerationEnvelope(result=response, mode=client.mode)
