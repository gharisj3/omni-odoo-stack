# Oracle OCI Deployment Notes

This project is designed for local or Oracle OCI Always Free deployment. It is a production-style portfolio architecture, not a claim of full production runtime certification.

## Suggested OCI Shape

- Ampere A1 Always Free
- Ubuntu 24.04
- Docker Engine + Docker Compose plugin

## Deployment Steps

1. Create the VM and open ports `22`, `80`, and `443`.
2. Install Docker and the Compose plugin.
3. Clone the repository.
4. Copy `.env.example` to `.env` and set real values.
5. Run `docker compose up -d`.
6. Point DNS to the host.
7. Update the Nginx TLS certificate paths once certificates exist.
8. Import the n8n workflows and register webhook endpoints.

## Recommended Verification

- `docker compose ps`
- `docker compose logs odoo --tail=100`
- `docker compose logs ai-middleware --tail=100`
- `python scripts/validate_project.py`
- `python scripts/smoke_test_ai.py --base-url http://localhost/ai`
