# Odoo Modules

The custom business logic lives only in [odoo/addons](E:\odoo\omni-odoo-stack\odoo\addons). Core Odoo source remains untouched in `odoo-source`.

## Installation Order

1. `omni_crm`
2. `omni_whatsapp`
3. `omni_ai`
4. `omni_automation`

## Module Summary

### `omni_crm`

- Extends CRM leads with scoring, AI summary fields, and WhatsApp shortcuts.
- Adds `POST /api/omni/lead`.
- Includes sample leads for demo walkthroughs.

### `omni_whatsapp`

- Stores inbound and outbound WhatsApp messages in Odoo.
- Adds webhook verification and inbound webhook handlers.
- Links messages to CRM leads and feeds automation logs.

### `omni_ai`

- Logs AI requests and responses.
- Sends lead data to the FastAPI middleware.
- Includes a cron job for periodic lead analysis.

### `omni_automation`

- Tracks cross-system automation events.
- Exposes endpoints for logging, vendor bill creation, and employee creation.
- Gives a dashboard-oriented monitoring view for the automation pipeline.
