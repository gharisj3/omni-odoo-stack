# Testing Guide

The repository includes syntax, JSON, and XML validation as well as middleware endpoint tests.

## Validation Commands

- `python scripts/validate_project.py`
- `python scripts/check_env.py --env-file .env`
- `pytest ai/tests -q`

## Smoke Test

Start the middleware or full stack, then run:

```bash
python scripts/smoke_test_ai.py --base-url http://localhost/ai
```

## What Is Verified

- Required files exist
- Python files compile
- n8n workflows and example payloads are valid JSON
- Odoo XML files are well-formed
- FastAPI endpoints work in mock mode without a Groq API key

## Known Limitation

Runtime boot verification depends on Docker being available on the local machine where you run the stack.
