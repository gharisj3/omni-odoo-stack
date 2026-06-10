"""Purpose: Validate project structure, Python syntax, JSON workflows/examples, and XML assets."""

from __future__ import annotations

import json
import py_compile
import sys
import xml.etree.ElementTree as etree
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    ROOT / "docker-compose.yml",
    ROOT / ".env.example",
    ROOT / "README.md",
    ROOT / "nginx" / "nginx.conf",
    ROOT / "odoo" / "config" / "odoo.conf",
    ROOT / "ai" / "middleware" / "main.py",
    ROOT / "n8n" / "workflows" / "whatsapp_lead.json",
]

PYTHON_DIRECTORIES = [
    ROOT / "ai",
    ROOT / "scripts",
    ROOT / "odoo" / "addons",
]

JSON_DIRECTORIES = [
    ROOT / "n8n" / "workflows",
    ROOT / "examples",
]

XML_DIRECTORIES = [
    ROOT / "odoo" / "addons",
]


def validate_required_files(errors: list[str]) -> None:
    """Confirm the core project files exist."""

    for path in REQUIRED_FILES:
        if not path.exists():
            errors.append(f"Missing required file: {path.relative_to(ROOT)}")


def validate_python(errors: list[str]) -> None:
    """Compile Python sources without importing project dependencies."""

    for directory in PYTHON_DIRECTORIES:
        if not directory.exists():
            continue
        for path in directory.rglob("*.py"):
            if "__pycache__" in path.parts:
                continue
            try:
                py_compile.compile(str(path), doraise=True)
            except py_compile.PyCompileError as exc:
                errors.append(f"Python syntax error in {path.relative_to(ROOT)}: {exc.msg}")


def validate_json(errors: list[str]) -> None:
    """Parse JSON workflow and example files."""

    for directory in JSON_DIRECTORIES:
        if not directory.exists():
            continue
        for path in directory.rglob("*.json"):
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                errors.append(f"JSON error in {path.relative_to(ROOT)}: {exc}")


def validate_xml(errors: list[str]) -> None:
    """Parse Odoo XML files for well-formedness."""

    for directory in XML_DIRECTORIES:
        if not directory.exists():
            continue
        for path in directory.rglob("*.xml"):
            try:
                etree.parse(path)
            except etree.ParseError as exc:
                errors.append(f"XML error in {path.relative_to(ROOT)}: {exc}")


def main() -> int:
    """Run all validation steps and print a concise result."""

    errors: list[str] = []
    validate_required_files(errors)
    validate_python(errors)
    validate_json(errors)
    validate_xml(errors)

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Validation passed: required files, Python, JSON, and XML checks are clean.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
