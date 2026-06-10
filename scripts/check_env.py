"""Purpose: Check required and optional environment variables for omni-odoo-stack."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

REQUIRED_VARS = [
    "POSTGRES_DB",
    "POSTGRES_USER",
    "POSTGRES_PASSWORD",
    "ODOO_ADMIN_PASSWD",
    "OMNI_API_KEY",
    "AI_SHARED_API_KEY",
]

OPTIONAL_VARS = [
    "GROQ_API_KEY",
    "META_WHATSAPP_TOKEN",
    "META_PHONE_NUMBER_ID",
    "LETSENCRYPT_EMAIL",
]


def load_env_file(env_file: Path) -> None:
    """Load a simple KEY=VALUE file into the process environment."""

    if not env_file.exists():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def main() -> int:
    """Report missing required variables and optional warnings."""

    parser = argparse.ArgumentParser(description="Check omni-odoo-stack environment variables.")
    parser.add_argument("--env-file", default=".env", help="Path to the environment file to inspect.")
    args = parser.parse_args()

    load_env_file(Path(args.env_file))

    missing_required = [name for name in REQUIRED_VARS if not os.getenv(name)]
    missing_optional = [name for name in OPTIONAL_VARS if not os.getenv(name)]

    if missing_required:
        print("Missing required environment variables:")
        for name in missing_required:
            print(f"- {name}")
    else:
        print("All required environment variables are present.")

    if missing_optional:
        print("Optional variables not set yet:")
        for name in missing_optional:
            print(f"- {name}")

    return 1 if missing_required else 0


if __name__ == "__main__":
    raise SystemExit(main())
