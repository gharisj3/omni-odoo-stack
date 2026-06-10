# Purpose: Common project commands for local setup, validation, and stack operations.

PYTHON ?= python
DOCKER_COMPOSE ?= docker compose

.PHONY: setup up down logs validate test-ai restart clean

setup:
	$(PYTHON) -m pip install -r ai/requirements.txt

up:
	$(DOCKER_COMPOSE) up -d

down:
	$(DOCKER_COMPOSE) down

logs:
	$(DOCKER_COMPOSE) logs -f

validate:
	$(PYTHON) scripts/validate_project.py

test-ai:
	$(PYTHON) scripts/smoke_test_ai.py

restart:
	$(DOCKER_COMPOSE) down
	$(DOCKER_COMPOSE) up -d

clean:
	$(PYTHON) -c "from pathlib import Path; [p.unlink() for p in Path('.').rglob('*.pyc') if p.is_file()]"
