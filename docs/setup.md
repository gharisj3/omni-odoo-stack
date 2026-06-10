# Omni Odoo Stack Setup Guide

This guide walks through local and Oracle OCI Always Free deployment for `omni-odoo-stack`. The stack is designed to stay within a $0 infrastructure budget while still demonstrating a realistic ERP, automation, and AI integration story.

## Prerequisites

- Docker Engine 26+ and Docker Compose
- Git
- An Oracle OCI Always Free Ubuntu 24.04 VM or a local machine
- Meta Cloud API test number and webhook configuration
- Groq API key on the free tier

## Local Setup

1. Copy `.env.example` to `.env` and replace every secret with real values.
2. Confirm `AI_SHARED_API_KEY`, `OMNI_API_KEY`, `META_VERIFY_TOKEN`, `META_WHATSAPP_TOKEN`, and `GROQ_API_KEY` are set.
3. Start the stack:

```bash
docker compose up -d
```

4. Open Odoo at `http://localhost`.
5. Open n8n at `http://localhost/n8n/`.
6. Confirm AI middleware health:

```bash
curl http://localhost/ai/health
```

## Odoo Module Installation

1. Log in as the Odoo administrator.
2. Enable developer mode.
3. Update the apps list.
4. Install the modules in this order:
   - `omni_crm`
   - `omni_whatsapp`
   - `omni_ai`
   - `omni_automation`

## n8n Workflow Import

1. Open the n8n editor.
2. Import the three JSON files from `n8n/workflows/`.
3. Map credentials and environment variables for:
   - Odoo HTTP endpoints
   - FastAPI middleware
   - Meta WhatsApp Cloud API
4. Activate each workflow after webhook URLs are registered in Meta.

## Oracle OCI Always Free Notes

- Use an Ampere A1 instance with Ubuntu 24.04.
- Open ports `80`, `443`, and `22` in the VCN security list.
- Install Docker Engine and Docker Compose plugin from the official Docker repository.
- Point DNS at the public IP, then replace the TLS certificate paths in `nginx/nginx.conf` with real Let's Encrypt material.
- Use a reverse proxy path strategy:
  - `/` for Odoo
  - `/n8n/` for n8n
  - `/ai/` for the middleware

## Operational Checks

- `docker compose ps`
- `docker compose logs odoo --tail=100`
- `docker compose logs ai-middleware --tail=100`
- `docker compose logs n8n --tail=100`
- `curl http://localhost/ai/health`
- `curl -X POST http://localhost/api/omni/lead ...`

