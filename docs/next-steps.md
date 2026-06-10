# Next Steps

## Runtime Docker Boot Verification Checklist

1. Confirm Docker is installed and `docker compose` is available.
2. Copy `.env.example` to `.env`.
3. Start the stack with `docker compose up -d`.
4. Check `docker compose ps`.
5. Check service logs for `db`, `odoo`, `ai-middleware`, `n8n`, and `nginx`.
6. Verify `http://localhost`, `http://localhost/n8n/`, and `http://localhost/ai/health`.
7. Install custom Odoo modules and exercise sample payloads.

## Recommended Screenshots

- CRM lead with AI summary
- WhatsApp message log
- AI request log
- Automation dashboard
- n8n canvas per workflow
- GitHub repo landing page

## Suggested Demo Video Flow

1. Show the architecture overview in the README.
2. Start from an inbound WhatsApp lead example.
3. Show n8n receiving the payload.
4. Show Odoo lead creation and AI summary.
5. Show invoice extraction and vendor bill draft creation.
6. Show HR onboarding workflow and final automation logs.

## Possible Future Modules

- vendor payment automation
- inventory alert automation
- sales order approval AI assistant
- invoice OCR pipeline
- FCCS/Fusion integration connector mock
