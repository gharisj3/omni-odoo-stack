# Omni Odoo Stack Architecture

`omni-odoo-stack` is a portfolio system that demonstrates how a free Odoo Community ERP can sit at the center of a modern automation architecture without requiring paid SaaS dependencies.

## System Overview

- Odoo 19 Community manages CRM, ERP records, and custom automation logs.
- PostgreSQL 16 stores transactional data for Odoo.
- FastAPI provides a controlled AI boundary for Groq-backed inference.
- n8n orchestrates webhook-driven workflows and external messaging.
- Nginx provides the single public ingress path, SSL termination, and reverse proxy routing.
- Meta WhatsApp Cloud API serves as the user-facing communication channel.

## Runtime Flow

1. A WhatsApp message or form submission reaches a webhook.
2. n8n normalizes the payload and sends it into Odoo.
3. Odoo creates or updates the business object and records the interaction.
4. Odoo or n8n calls the FastAPI middleware for AI enrichment.
5. The middleware enforces request validation, calls Groq, and returns structured JSON.
6. Odoo stores the analysis result and automation logs.
7. n8n sends replies or downstream notifications through Meta WhatsApp Cloud API.

## Module Responsibilities

- `omni_crm`: Lead scoring, AI summary fields, and a lead intake API.
- `omni_whatsapp`: Message persistence and inbound webhook handling.
- `omni_ai`: AI request logging, middleware calls, and scheduled lead analysis.
- `omni_automation`: Cross-system pipeline logging and dashboarding.

## Deployment Design Choices

- The project uses Odoo Community and n8n self-hosted to avoid recurring software licensing costs.
- FastAPI is intentionally isolated from Odoo so AI logic can evolve without modifying ERP core code.
- Nginx front-loads operational concerns like compression, TLS, and path routing.
- Environment variables isolate secrets and deployment-specific values from source control.

