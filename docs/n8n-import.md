# n8n Workflow Import Guide

The repository includes three workflow exports in [n8n/workflows](E:\odoo\omni-odoo-stack\n8n\workflows):

- `whatsapp_lead.json`
- `invoice_processor.json`
- `hr_onboarding.json`

## Import Steps

1. Start the stack and open `http://localhost/n8n/`.
2. Log in with `N8N_BASIC_AUTH_USER` and `N8N_BASIC_AUTH_PASSWORD`.
3. Use `Import from File`.
4. Import each JSON workflow.
5. Review the sticky note node in each workflow for required environment variables.
6. Activate the workflow only after webhook URLs and WhatsApp credentials are ready.

## Required Environment Variables

- `OMNI_ODOO_BASE_URL`
- `OMNI_AI_BASE_URL`
- `OMNI_API_KEY`
- `AI_SHARED_API_KEY`
- `META_GRAPH_API_BASE_URL`
- `META_WHATSAPP_TOKEN`
- `META_PHONE_NUMBER_ID`

## Sample Test Payloads

- Lead and WhatsApp flow: [examples/whatsapp_webhook_payload.json](E:\odoo\omni-odoo-stack\examples\whatsapp_webhook_payload.json)
- Invoice flow: [examples/invoice_payload.json](E:\odoo\omni-odoo-stack\examples\invoice_payload.json)
- HR flow: [examples/hr_onboarding_payload.json](E:\odoo\omni-odoo-stack\examples\hr_onboarding_payload.json)
