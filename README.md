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
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED)
![n8n](https://img.shields.io/badge/n8n-Self--Hosted-EA4B71)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688)
![Groq](https://img.shields.io/badge/Groq-Llama3--8B-0A0A0A)
![License MIT](https://img.shields.io/badge/License-MIT-green)

## Overview

`omni-odoo-stack` is a complete portfolio project that demonstrates a realistic $0 ERP implementation stack built around Odoo 19 Community, PostgreSQL, n8n automation, FastAPI middleware, Groq AI, and Meta WhatsApp Cloud API. The goal is to show how modern ERP customization, automation engineering, and AI-enriched workflows can be delivered without paid infrastructure or enterprise licensing.

The project is deployable on Oracle OCI Always Free Tier or any local machine that can run Docker. It keeps the upstream Odoo source pristine and places all custom behavior in installable addons under `odoo/addons/`.

## Architecture Diagram

```text
                   +-------------------------------+
                   |         Internet Users        |
                   | WhatsApp, Forms, Admin Staff |
                   +---------------+---------------+
                                   |
                                   v
                      +----------------------------+
                      |           Nginx            |
                      | TLS, gzip, reverse proxy   |
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
            | FastAPI Middleware  +------>+ Groq Free Tier   |
            | validation + auth   |       | llama3-8b-8192   |
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
| Odoo Community | 19.0 | ERP, CRM, business logic | $0 |
| PostgreSQL | 16 | Transactional database | $0 |
| Python | 3.12 | Middleware runtime | $0 |
| FastAPI | 0.115.0 | AI API gateway | $0 |
| Groq | Free tier | LLM inference | $0 |
| n8n | 1.95.3 | Workflow automation | $0 |
| Nginx | 1.27 | Reverse proxy and TLS ingress | $0 |
| Meta WhatsApp Cloud API | Free tier | Messaging channel | $0 |
| Oracle OCI Ampere A1 | Always Free | Hosting target | $0 |

## Features

- Odoo 19 Community scaffold cloned directly from upstream branch `19.0`
- Production-style Docker Compose stack with PostgreSQL, Odoo, FastAPI, n8n, and Nginx
- Custom CRM extension with lead scoring, AI summary storage, and a lead intake API
- WhatsApp webhook bridge with message history stored inside Odoo
- AI request logging module with scheduled lead analysis
- Automation dashboard and logging model for full pipeline visibility
- FastAPI middleware with validated schemas and Groq-backed structured outputs
- Three importable n8n workflows for lead capture, invoice processing, and HR onboarding
- OCI-ready deployment pattern using only free-tier components

## Phase Breakdown

### Phase 1: Odoo 19 + PostgreSQL + Docker setup

- Upstream Odoo 19 Community source cloned into `odoo-source`
- Docker Compose services for Odoo, PostgreSQL, AI middleware, n8n, and Nginx
- Centralized environment variables and production-minded Odoo config

### Phase 2: 4 custom Odoo modules

- `omni_crm`
- `omni_whatsapp`
- `omni_ai`
- `omni_automation`

### Phase 3: FastAPI + Groq AI middleware

- `POST /analyze/lead`
- `POST /extract/invoice`
- `POST /generate/message`
- `GET /health`

### Phase 4: n8n automation workflows

- WhatsApp lead intake pipeline
- Invoice processing pipeline
- HR onboarding workflow

## Quick Start

1. `cd omni-odoo-stack`
2. `cp .env.example .env`
3. Edit `.env` with real Groq, Meta, and API keys
4. `docker compose up -d`
5. Open `http://localhost`
6. Install `omni_crm`, `omni_whatsapp`, `omni_ai`, and `omni_automation`
7. Open `http://localhost/n8n/` and import the workflow JSON files
8. Test `http://localhost/ai/health`
9. Trigger a sample lead through `POST /api/omni/lead`

## Environment Variables

| Variable | Purpose |
| --- | --- |
| `POSTGRES_DB` | Odoo PostgreSQL database name |
| `POSTGRES_USER` | PostgreSQL username |
| `POSTGRES_PASSWORD` | PostgreSQL password |
| `ODOO_ADMIN_PASSWD` | Odoo admin/master password |
| `ODOO_DB_HOST` | Odoo database host |
| `ODOO_DB_PORT` | Odoo database port |
| `ODOO_DB_USER` | Odoo database user |
| `ODOO_DB_PASSWORD` | Odoo database password |
| `ODOO_DB_NAME` | Odoo database name |
| `ODOO_PROXY_MODE` | Enable reverse proxy headers in Odoo |
| `ODOO_HTTP_PORT` | Main Odoo HTTP port |
| `ODOO_LONGPOLLING_PORT` | Odoo longpolling port |
| `ODOO_LOG_LEVEL` | Odoo log verbosity |
| `ODOO_WORKERS` | Odoo worker count |
| `OMNI_API_KEY` | Shared key for n8n to Odoo custom APIs |
| `OMNI_AI_ENDPOINT` | Base URL for AI middleware from Odoo |
| `AI_SHARED_API_KEY` | Shared key for Odoo or n8n to FastAPI |
| `GROQ_API_KEY` | Groq free-tier key |
| `META_VERIFY_TOKEN` | Meta webhook verification token |
| `META_WHATSAPP_TOKEN` | Meta WhatsApp Cloud API access token |
| `META_PHONE_NUMBER_ID` | Meta sender phone number id |
| `N8N_BASIC_AUTH_USER` | n8n login username |
| `N8N_BASIC_AUTH_PASSWORD` | n8n login password |
| `N8N_HOST` | Public n8n host |
| `N8N_PROTOCOL` | Public n8n scheme |
| `N8N_EDITOR_BASE_URL` | n8n base editor URL |
| `N8N_WEBHOOK_URL` | n8n webhook base URL |
| `N8N_ENCRYPTION_KEY` | n8n encryption secret |
| `LETSENCRYPT_EMAIL` | Certificate registration email |
| `NGINX_HOST` | Server hostname |

## API Documentation

### Odoo endpoints

`POST /api/omni/lead`

Request:

```json
{
  "name": "Northwind Foods ERP Project",
  "company": "Northwind Foods",
  "email": "ops@northwind.example",
  "phone": "+923001234567",
  "description": "Need CRM, accounting, and warehouse automation rollout."
}
```

Response:

```json
{
  "id": 42,
  "name": "Northwind Foods ERP Project",
  "score": 8,
  "priority": "high"
}
```

`GET /whatsapp/webhook`

- Used for Meta webhook verification.

`POST /whatsapp/webhook`

- Receives inbound WhatsApp messages and stores them in `omni.whatsapp.message`.

`POST /api/omni/automation/log`

- Creates automation audit events from n8n or external systems.

`POST /api/omni/vendor-bill`

- Creates a draft vendor bill from structured invoice extraction payloads.

`POST /api/omni/hr/employee`

- Creates a new employee record for onboarding workflows.

### FastAPI endpoints

`GET /ai/health`

Response:

```json
{
  "status": "ok",
  "service": "omni-odoo-stack-ai"
}
```

`POST /ai/analyze/lead`

Request:

```json
{
  "name": "Acme Distribution ERP",
  "email": "owner@acme.example",
  "phone": "+923009999999",
  "description": "Need Odoo migration, warehouse automation, and WhatsApp lead capture.",
  "company": "Acme Distribution"
}
```

Response:

```json
{
  "score": 9,
  "summary": "Well-scoped distribution ERP opportunity with clear automation upside.",
  "next_action": "Schedule a discovery call and gather process maps.",
  "priority": "high"
}
```

`POST /ai/extract/invoice`

Request:

```json
{
  "raw_text": "Vendor: Atlas Supplies\nDate: 2026-06-01\nTotal: 1550 USD\n1 x Steel Shelving 1550"
}
```

Response:

```json
{
  "vendor": "Atlas Supplies",
  "amount": 1550,
  "date": "2026-06-01",
  "line_items": [
    {
      "description": "Steel Shelving",
      "quantity": 1,
      "unit_price": 1550,
      "total": 1550
    }
  ],
  "currency": "USD"
}
```

`POST /ai/generate/message`

Request:

```json
{
  "context": "A prospect asked when they can get a proposal.",
  "customer_name": "Ayesha",
  "intent": "follow_up"
}
```

Response:

```json
{
  "message": "Hi Ayesha, thanks for reaching out. We can send your proposal after a short discovery call tomorrow.",
  "tone": "professional",
  "suggested_actions": [
    "Book discovery call",
    "Collect current process notes"
  ]
}
```

## Demo Scenarios

### Scenario 1: WhatsApp lead to CRM to AI

1. Prospect messages the Meta WhatsApp number.
2. Meta posts the event to n8n.
3. n8n normalizes the payload and creates the lead in Odoo.
4. AI middleware generates a response and Odoo logs the interaction.
5. Capture the CRM lead record, AI summary, and automation log after the workflow completes.

### Scenario 2: Invoice capture through WhatsApp

1. Vendor sends invoice text or OCR output.
2. n8n forwards the text to FastAPI for extraction.
3. Odoo receives a vendor bill creation request.
4. Capture the imported vendor bill draft and the matching automation audit log.

### Scenario 3: HR onboarding automation

1. HR submits a new employee form.
2. n8n creates the employee in Odoo.
3. FastAPI generates the welcome message.
4. WhatsApp notifications go to the employee and HR manager.
5. Capture the employee record, welcome message, and HR notification audit trail.

## Deployment Guide

### Oracle OCI Always Free step by step

1. Create an Ampere A1 VM with Ubuntu 24.04.
2. Assign a reserved public IP if available.
3. Open ports `80` and `443` in the VCN security rules.
4. Install Docker Engine and Docker Compose plugin.
5. Clone this repository.
6. Copy `.env.example` to `.env` and insert real values.
7. Run `docker compose up -d`.
8. Point DNS to the VM.
9. Provision Let's Encrypt certificates and update `nginx/nginx.conf`.
10. Import the n8n workflows and register the webhook endpoints in Meta.

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
WhatsApp: +92 303 2712221

### Services Available

- Custom Odoo module development (v14-v19)
- n8n workflow automation
- AI/LLM middleware for ERP systems
- Oracle OCI / EPM FCCS / Fusion integrations
- PostgreSQL optimization
- WhatsApp API integration
- White-label subcontract work for Odoo partners

> "Let's start with a small scoped task and let the work speak for itself."

## License

MIT License

## Contributing

Contributions are welcome through issues, design discussions, workflow improvements, deployment hardening, and additional open-source Odoo integrations. If you open a pull request, include:

- A clear problem statement
- Screenshots or logs for behavior changes
- Test steps for Odoo, FastAPI, or n8n changes
- Notes on any new environment variables or operational impact
