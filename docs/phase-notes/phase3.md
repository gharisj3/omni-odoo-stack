# Phase 3 Notes

## What Was Built

Phase 3 delivered the FastAPI middleware, Pydantic v2 schemas, and a Groq client with retries and JSON-only completions.

## Why These Decisions Were Made

- FastAPI is lightweight, production-proven, and straightforward to document.
- Pydantic v2 keeps request and response contracts explicit.
- A separate middleware service allows AI prompts and models to change without destabilizing Odoo.

## Technical Challenges Solved

- Enforcing structured outputs from a general-purpose LLM.
- Sharing authentication across n8n and Odoo through a simple API key scheme.
- Logging token usage and request failures in a way that can be surfaced operationally.

## How To Test This Phase

- Install middleware requirements or start the container.
- Call `GET /health`.
- Call `POST /analyze/lead`, `POST /extract/invoice`, and `POST /generate/message` with `X-API-Key`.
- Confirm Odoo AI requests are created when lead analysis is triggered.

## What Comes Next

Phase 4 ties the whole stack together with importable n8n workflows for lead capture, invoice processing, and HR onboarding.

