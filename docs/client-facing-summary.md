# Client-Facing Summary

`omni-odoo-stack` is a proof-of-work project that demonstrates how an ERP system, workflow automation engine, messaging channel, and AI middleware can work together in one practical architecture.

## What Problem It Solves

Many businesses collect leads, invoices, and onboarding requests through disconnected channels such as WhatsApp, email, and forms. This project shows how those touchpoints can be routed into Odoo, enriched by automation, and reviewed through a structured back-office process.

## Who It Is For

- Odoo partners
- ERP implementation firms
- Operations teams
- Businesses that want WhatsApp-connected workflows
- Teams evaluating AI-assisted backend automation

## How The Stack Works

- Odoo holds the core business records.
- n8n coordinates webhook-based workflows and external notifications.
- WhatsApp acts as a real customer-facing communication channel.
- FastAPI sits between the ERP and the AI model so prompts, validation, and fail-safe behavior remain controlled.

## Why Separate AI Middleware From Odoo

Keeping AI outside Odoo makes it easier to:

- validate payloads before model calls
- switch between live and mock/demo mode
- change prompts or models without changing ERP internals
- expose AI logic to multiple systems, not just Odoo

## Why This Matters As Portfolio Work

This project demonstrates backend architecture capability, not only feature coding. It shows:

- Odoo customization
- workflow orchestration
- API design
- environment-driven deployment
- AI boundary design
- client-facing technical documentation
