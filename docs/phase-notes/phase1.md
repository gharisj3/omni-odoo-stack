# Phase 1 Notes

## What Was Built

Phase 1 established the shared runtime: Docker Compose orchestration, PostgreSQL 16, Odoo 19 Community, n8n, FastAPI middleware, and Nginx reverse proxying.

## Why These Decisions Were Made

- Docker Compose keeps the local and OCI flows aligned.
- PostgreSQL 16 is the natural production-grade database choice for Odoo.
- Nginx gives one ingress path and a clean place to add TLS.
- Environment-driven config keeps secrets out of version control.

## Technical Challenges Solved

- Preserving the upstream Odoo codebase while keeping all custom work in `odoo/addons`.
- Designing path-based proxy routing so Odoo, n8n, and FastAPI can coexist behind one host.
- Keeping the stack free-tier friendly without introducing paid services.

## How To Test This Phase

- Run `docker compose up -d`.
- Confirm `db`, `odoo`, `ai-middleware`, `n8n`, and `nginx` are healthy.
- Open `http://localhost`.
- Call `GET /ai/health` through Nginx.

## What Comes Next

Phase 2 adds the four custom Odoo modules that convert the infrastructure into a portfolio-worthy ERP extension stack.

