# Phase 4 Notes

## What Was Built

Phase 4 added three n8n workflows: WhatsApp lead intake, invoice processing, and HR onboarding automation.

## Why These Decisions Were Made

- n8n shows real orchestration capability without adding paid middleware.
- Workflow JSON exports make the project instantly demoable.
- Externalized HTTP calls keep the workflows understandable and easy to adapt to real credentials.

## Technical Challenges Solved

- Modeling realistic webhook-driven flows without coupling them tightly to a single deployment.
- Creating an error logging path back into Odoo for automation visibility.
- Balancing demo clarity with production-style payload handling.

## How To Test This Phase

- Import each JSON workflow into n8n.
- Register the webhook URLs with Meta or use manual webhook POSTs.
- Confirm Odoo records are created and automation logs are written.
- Check response messages and audit trail behavior in the `Automation` menu.

## What Comes Next

The next natural step is portfolio polish: screenshots, a short demo video, and a public GitHub release with deployment notes from a live OCI rollout.

