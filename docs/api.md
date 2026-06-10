# API Reference

This document summarizes the HTTP interfaces exposed by the project for demos, automation, and verification.

## FastAPI Middleware

Base URL:
- Direct container: `http://ai-middleware:8000`
- Through Nginx: `http://localhost/ai`

Authentication:
- Header: `X-API-Key`
- Value: `AI_SHARED_API_KEY`

Endpoints:
- `GET /health`
- `POST /analyze/lead`
- `POST /extract/invoice`
- `POST /generate/message`

Example:

```bash
curl -X POST http://localhost/ai/analyze/lead \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $AI_SHARED_API_KEY" \
  -d @examples/lead_payload.json
```

Mock mode:
- If `AI_MOCK_MODE=true` or `GROQ_API_KEY` is missing, the middleware returns deterministic mock responses.
- This makes the project demo-safe without paid AI access.

## Odoo Custom Endpoints

Base URL:
- Direct container: `http://odoo:8069`
- Through Nginx: `http://localhost`

Authentication:
- Header: `X-Omni-API-Key`
- Value: `OMNI_API_KEY`

Endpoints:
- `POST /api/omni/lead`
- `POST /api/omni/automation/log`
- `POST /api/omni/vendor-bill`
- `POST /api/omni/hr/employee`
- `GET /whatsapp/webhook`
- `POST /whatsapp/webhook`

Example:

```bash
curl -X POST http://localhost/api/omni/lead \
  -H "Content-Type: application/json" \
  -H "X-Omni-API-Key: $OMNI_API_KEY" \
  -d @examples/lead_payload.json
```
