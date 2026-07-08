# OMNI ODOO STACK

```text
   ____  __  __ _   _ ___    ___   ___  ____   ___   ___    ____ _____  _    ____ _  __
  / __ \|  \/  | \ | |_ _|  / _ \ / _ \|  _ \ / _ \ / _ \  / ___|_   _|/ \  / ___| |/ /
 | |  | | |\/| |  \| || |  | | | | | | | | | | | | | | | | \___ \ | | / _ \| |   | ' /
 | |__| | |  | | |\  || |  | |_| | |_| | |_| | |_| | |_| |  ___) || |/ ___ \ |___| . \
  \____/|_|  |_|_| \_|___|  \___/ \___/|____/ \___/ \___/  |____/ |_/_/   \_\____|_|\_\
```

![Odoo 19](https://img.shields.io/badge/Odoo-19-714B67)
![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB)
![Docker Compose](https://img.shields.io/badge/Docker-Compose-2496ED)
![n8n](https://img.shields.io/badge/n8n-Self--Hosted-EA4B71)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688)
![Groq](https://img.shields.io/badge/Groq-Llama3--8B-0A0A0A)
![MIT License](https://img.shields.io/badge/License-MIT-green)

## Project Headline

`omni-odoo-stack` is a production-style portfolio architecture for **Odoo backend automation**, **WhatsApp-connected workflows**, **AI middleware**, and **n8n orchestration**. It is designed for local or Oracle OCI Always Free deployment and packaged as a proof-of-work asset for ERP customization and automation engineering.

## Business Explanation

This project demonstrates how inbound leads, invoice text, and HR onboarding requests can move through one connected backend stack:

- WhatsApp or webhooks collect the request
- n8n orchestrates the workflow
- Odoo stores the core business record
- FastAPI validates and enriches data through AI
- automation logs stay visible inside Odoo

The result is a clean demo of how ERP, messaging, workflow automation, and AI can work together without paid infrastructure or enterprise licensing.

## Architecture Overview

```text
                   +-------------------------------+
                   |         Internet Users        |
                   | WhatsApp, Forms, Admin Staff |
                   +---------------+---------------+
                                   |
                                   v
                      +----------------------------+
                      |           Nginx            |
                      | TLS-ready reverse proxy    |
                      +-----+---------------+------+
                            |               |
               +------------+--+         +--+----------------+
               | Odoo 19 ERP  |         | n8n Workflow Hub  |
               | omni addons  |         | webhook pipelines |
               +------+-------+         +---------+---------+
                      |                           |
                      |                           v
                      |                 +--------------------+
                      |                 | Meta WhatsApp API  |
                      |                 +--------------------+
                      |
                      v
            +---------------------+       +------------------+
            | FastAPI Middleware  +------>+ Groq or Mock AI  |
            | validation + auth   |       | demo-safe mode   |
            +----------+----------+       +------------------+
                       |
                       v
               +---------------+
               | PostgreSQL 16 |
               +---------------+
```

## Tech Stack

| Component | Version | Purpose | Cost |
| --- | --- | --- | --- |
| Odoo Community | 19.0 | ERP, CRM, business records | $0 |
| PostgreSQL | 16 | Odoo database | $0 |
| FastAPI | 0.115.0 | AI middleware and API boundary | $0 |
| Groq | Free tier | Live LLM inference | $0 |
| Mock AI mode | Built-in | Demo-safe fallback without API access | $0 |
| n8n | 1.95.3 | Workflow automation | $0 |
| Nginx | 1.27 | Reverse proxy and ingress | $0 |
| Docker Compose | Current | Local and OCI stack orchestration | $0 |
| Meta WhatsApp Cloud API | Free tier | Messaging channel | $0 |
| Oracle OCI Ampere A1 | Always Free | Recommended hosting target | $0 |

## What Each Service Does

- `db`: persists Odoo data in PostgreSQL
- `odoo`: runs Odoo 19 Community with custom addons under `odoo/addons`
- `ai-middleware`: exposes validated AI endpoints with live or mock mode
- `n8n`: runs webhook-driven workflows for CRM, invoices, and onboarding
- `nginx`: exposes Odoo, n8n, and AI through one public entry point

## Odoo Modules

### `omni_crm`

- Adds lead scoring, AI analysis fields, and WhatsApp shortcuts to CRM leads
- Exposes `POST /api/omni/lead`

### `omni_whatsapp`

- Stores inbound and outbound WhatsApp messages in Odoo
- Exposes Meta webhook verification and message intake endpoints

### `omni_ai`

- Logs AI requests and responses
- Calls the FastAPI middleware from Odoo
- Includes a cron job for background lead analysis

### `omni_automation`

- Tracks workflow events and failures
- Exposes helper endpoints for vendor bill and employee creation
- Provides automation monitoring views inside Odoo

## n8n Workflows

### `whatsapp_lead.json`

- Receives WhatsApp webhook payloads
- Creates a lead in Odoo
- Calls the AI middleware for a reply
- Sends a confirmation message
- Logs failures back into Odoo

### `invoice_processor.json`

- Accepts invoice text
- Extracts structured invoice fields through FastAPI
- Creates a draft vendor bill in Odoo
- Sends confirmation to the sender

### `hr_onboarding.json`

- Receives onboarding data
- Creates an employee in Odoo
- Generates a welcome message
- Notifies both employee and HR manager via WhatsApp

## AI Middleware

The middleware lives in [ai/middleware](E:\odoo\omni-odoo-stack\ai\middleware) and provides:

- `GET /health`
- `POST /analyze/lead`
- `POST /extract/invoice`
- `POST /generate/message`

Key behavior:

- Pydantic v2 request and response validation
- API key authentication via `X-API-Key`
- live Groq mode when `GROQ_API_KEY` exists
- mock mode when `AI_MOCK_MODE=true` or no Groq key is configured
- request validation logging and consistent JSON errors

## Local Setup

1. Clone the repository.
2. Copy `.env.example` to `.env`.
3. Fill in the required values.
4. Start the stack:

```bash
docker compose up -d
```

5. Open:

- `http://localhost` for Odoo
- `http://localhost/n8n/` for n8n
- `http://localhost/ai/health` for middleware health

## Docker Commands

```bash
docker compose up -d
docker compose ps
docker compose logs -f
docker compose down
```

Or with the Makefile:

```bash
make up
make logs
make down
make validate
make test-ai
```

## Environment Setup

Core variables to set:

- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `ODOO_ADMIN_PASSWD`
- `OMNI_API_KEY`
- `AI_SHARED_API_KEY`

Optional for live integrations:

- `GROQ_API_KEY`
- `META_WHATSAPP_TOKEN`
- `META_PHONE_NUMBER_ID`
- `LETSENCRYPT_EMAIL`

## API Examples

Analyze a lead:

```bash
curl -X POST http://localhost/ai/analyze/lead \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $AI_SHARED_API_KEY" \
  -d @examples/lead_payload.json
```

Create a lead in Odoo:

```bash
curl -X POST http://localhost/api/omni/lead \
  -H "Content-Type: application/json" \
  -H "X-Omni-API-Key: $OMNI_API_KEY" \
  -d @examples/lead_payload.json
```

## Demo Flow

### WhatsApp Lead Demo

1. Send or simulate a WhatsApp webhook payload.
2. n8n normalizes the message and calls Odoo.
3. Odoo stores the lead.
4. FastAPI returns a structured reply in live or mock mode.
5. Odoo and n8n store the workflow audit trail.

### Invoice Demo

1. Send invoice text into the invoice workflow.
2. FastAPI extracts vendor bill fields.
3. Odoo creates a draft vendor bill record.
4. WhatsApp confirmation is sent back to the user.

### HR Demo

1. Submit onboarding payload.
2. Odoo creates the employee.
3. FastAPI generates the welcome message.
4. Notifications are sent and logged.

## Screenshots

Recommended screenshot targets are documented in [docs/screenshots.md](E:\odoo\omni-odoo-stack\docs\screenshots.md).

Suggested captures:

- CRM lead form with score and AI summary
- WhatsApp message history
- AI request log
- Automation dashboard
- n8n workflow canvases

## Validation and Verification

Syntax, JSON, and XML validation included:

```bash
python scripts/validate_project.py
python scripts/check_env.py --env-file .env
pytest ai/tests -q
```

Runtime verification instructions included:

- [docs/testing.md](E:\odoo\omni-odoo-stack\docs\testing.md)
- [docs/setup.md](E:\odoo\omni-odoo-stack\docs\setup.md)
- [docs/deployment-oci.md](E:\odoo\omni-odoo-stack\docs\deployment-oci.md)

## Known Limitation

This repository has been upgraded into a cleaner, more demo-ready architecture and includes syntax, JSON, XML, and middleware endpoint validation. It should be described as a **production-style portfolio architecture**, not a fully production-tested deployment, until the full Docker runtime stack has been booted and verified on a machine with Docker available.

## Portfolio Positioning

This project is useful as a public proof-of-work asset for:

- Odoo backend automation consulting
- n8n workflow engineering
- ERP middleware architecture
- WhatsApp-connected operational workflows
- AI-assisted business process design

## Built By

Muhammad Gharis Javed  
Odoo ERP & Backend Automation Specialist | 8+ Years Production Experience

This project was built as a live portfolio demonstrating real production-grade Odoo ERP customization, n8n automation, WhatsApp integration, and AI middleware engineering - all on a $0 infrastructure stack.

If you need similar work done for your business or Odoo partner firm:

Email: gharis@omni-academy.com  
LinkedIn: [https://www.linkedin.com/in/muhammad-gharis-javed-318266202/](https://www.linkedin.com/in/muhammad-gharis-javed-318266202/)  
GitHub: [https://github.com/gharisj3](https://github.com/gharisj3)  
Website: [https://www.omni-academy.com](https://www.omni-academy.com)  
Fiverr: [https://www.fiverr.com/sellers/muhammadghar709](https://www.fiverr.com/sellers/muhammadghar709)  
Contra: [https://contra.com/muhammad_gharis_j2g71vgn](https://contra.com/muhammad_gharis_j2g71vgn)  
WhatsApp : @muhammadgharis

## License

MIT License
