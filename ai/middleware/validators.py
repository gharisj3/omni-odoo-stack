"""Purpose: Pydantic v2 request and response models for the AI middleware."""

from __future__ import annotations

from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class LeadInput(BaseModel):
    """Incoming CRM lead payload for AI analysis."""

    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=2, max_length=120)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=32)
    description: str = Field(min_length=10, max_length=5000)
    company: str | None = Field(default=None, max_length=120)


class LeadAnalysis(BaseModel):
    """Structured AI analysis returned for a lead."""

    model_config = ConfigDict(str_strip_whitespace=True)

    score: int = Field(ge=1, le=10)
    summary: str = Field(min_length=10, max_length=1000)
    next_action: str = Field(min_length=5, max_length=300)
    priority: str = Field(pattern="^(low|medium|high|urgent)$")


class InvoiceInput(BaseModel):
    """Raw invoice text ready for extraction."""

    model_config = ConfigDict(str_strip_whitespace=True)

    raw_text: str = Field(min_length=20, max_length=12000)


class InvoiceLineItem(BaseModel):
    """Single extracted line item from an invoice."""

    model_config = ConfigDict(str_strip_whitespace=True)

    description: str = Field(min_length=1, max_length=250)
    quantity: int = Field(ge=1)
    unit_price: Decimal = Field(ge=0)
    total: Decimal = Field(ge=0)


class InvoiceData(BaseModel):
    """Structured invoice extraction output."""

    model_config = ConfigDict(str_strip_whitespace=True)

    vendor: str = Field(min_length=2, max_length=120)
    amount: Decimal = Field(ge=0)
    date: date
    line_items: list[InvoiceLineItem]
    currency: str = Field(min_length=3, max_length=3)


class MessageInput(BaseModel):
    """Context payload for WhatsApp message generation."""

    model_config = ConfigDict(str_strip_whitespace=True)

    context: str = Field(min_length=10, max_length=4000)
    customer_name: str = Field(min_length=2, max_length=120)
    intent: str = Field(min_length=2, max_length=120)


class MessageOutput(BaseModel):
    """Generated WhatsApp response and suggested actions."""

    model_config = ConfigDict(str_strip_whitespace=True)

    message: str = Field(min_length=10, max_length=1000)
    tone: str = Field(pattern="^(friendly|professional|empathetic|urgent)$")
    suggested_actions: list[str] = Field(min_length=1, max_length=5)

