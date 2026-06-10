# Setup Guide

## Prerequisites

- Docker Engine with Docker Compose
- Git
- A `.env` file created from `.env.example`

Optional:

- Groq API key for live AI mode
- Meta WhatsApp Cloud API credentials

## Quick Start

1. Copy `.env.example` to `.env`.
2. Fill in at least:
   - `POSTGRES_DB`
   - `POSTGRES_USER`
   - `POSTGRES_PASSWORD`
   - `ODOO_ADMIN_PASSWD`
   - `OMNI_API_KEY`
   - `AI_SHARED_API_KEY`
3. Start the stack:

```bash
docker compose up -d
```

4. Verify service health:

```bash
docker compose ps
python scripts/validate_project.py
python scripts/smoke_test_ai.py --base-url http://localhost/ai
```

5. Open:

- `http://localhost`
- `http://localhost/n8n/`
- `http://localhost/ai/health`

## Odoo Module Installation

Install the custom modules in this order:

1. `omni_crm`
2. `omni_whatsapp`
3. `omni_ai`
4. `omni_automation`

## n8n Workflow Import

Follow [docs/n8n-import.md](E:\odoo\omni-odoo-stack\docs\n8n-import.md) and use the sample payloads in [examples](E:\odoo\omni-odoo-stack\examples).

## Mock Mode

If you do not have a Groq key yet:

- keep `AI_MOCK_MODE=true`
- leave `GROQ_API_KEY` blank

The middleware will still run and return deterministic demo responses.
