# Architecture

`omni-odoo-stack` is structured as a production-style portfolio architecture that keeps ERP logic, workflow orchestration, messaging, and AI concerns separated but connected.

## Core Design

- Odoo is the source of truth for CRM, automation logs, AI requests, and downstream operational records.
- n8n coordinates webhook-based automation and outbound notifications.
- FastAPI acts as a strict boundary for AI requests so prompt logic and model fallback behavior remain outside Odoo.
- Nginx presents the stack through one ingress layer for local demos or OCI deployment.
- PostgreSQL stores Odoo application data.

## Service Relationships

- `db` supports Odoo persistence.
- `odoo` exposes business records and custom APIs.
- `ai-middleware` handles validated AI operations.
- `n8n` consumes webhook events and calls Odoo plus the middleware.
- `nginx` routes `/`, `/n8n/`, and `/ai/`.

## Demo-Safe AI Mode

The middleware supports:

- live mode with Groq when `GROQ_API_KEY` is configured
- mock mode when the key is missing or `AI_MOCK_MODE=true`

This allows the project to stay demo-ready even without external paid or rate-limited AI access.

## Addon Boundaries

- `omni_crm`: CRM enhancements and lead intake
- `omni_whatsapp`: webhook and message storage
- `omni_ai`: AI request logging and lead enrichment
- `omni_automation`: orchestration logging and helper APIs
