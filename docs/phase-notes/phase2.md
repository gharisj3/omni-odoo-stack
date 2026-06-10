# Phase 2 Notes

## What Was Built

Phase 2 added four Odoo 19 addons: `omni_crm`, `omni_whatsapp`, `omni_ai`, and `omni_automation`.

## Why These Decisions Were Made

- Splitting by concern keeps the architecture modular and easier to demo.
- Extending native `crm.lead` avoids reinventing core CRM behavior.
- Logging models in `omni_ai` and `omni_automation` make the system observable and easier to debug.

## Technical Challenges Solved

- Coordinating dependencies without modifying Odoo core.
- Designing controllers that can be called by n8n and Meta webhooks.
- Exposing meaningful views and menus so the stack feels like a usable product, not just backend code.

## How To Test This Phase

- Install the modules in order from Apps.
- Open CRM leads and confirm score, AI summary fields, and WhatsApp button visibility.
- Visit WhatsApp message history and Automation dashboard menus.
- Send a JSON payload to `POST /api/omni/lead` with a valid `X-Omni-API-Key`.

## What Comes Next

Phase 3 introduces the standalone AI boundary with validated FastAPI endpoints and Groq integration.

