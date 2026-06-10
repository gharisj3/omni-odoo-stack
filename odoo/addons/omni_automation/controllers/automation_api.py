"""Purpose: Provide an ingestion endpoint for external automation error and event logs."""

from __future__ import annotations

import json
import os

from odoo import http
from odoo.http import request


class OmniAutomationAPIController(http.Controller):
    """API endpoint for automation event ingestion from tools like n8n."""

    def _is_authorized(self) -> bool:
        """Validate the shared API key used by external workflow tools."""

        expected_key = os.getenv("OMNI_API_KEY")
        received_key = request.httprequest.headers.get("X-Omni-API-Key")
        return bool(expected_key and expected_key == received_key)

    @staticmethod
    def _json_response(payload: dict, status_code: int):
        """Return a JSON response with a consistent content type."""

        return request.make_response(
            json.dumps(payload),
            headers=[("Content-Type", "application/json")],
            status=status_code,
        )

    def _parse_payload(self) -> dict:
        """Parse the incoming request body as JSON."""

        return json.loads(request.httprequest.data.decode("utf-8") or "{}")

    @http.route("/api/omni/automation/log", type="http", auth="public", methods=["POST"], csrf=False)
    def create_log(self, **_kwargs):
        """Store an automation event sent by an external workflow engine."""

        if not self._is_authorized():
            return self._json_response({"error": "Unauthorized"}, 401)

        try:
            payload = self._parse_payload()
        except json.JSONDecodeError:
            return self._json_response({"error": "Invalid JSON payload"}, 400)
        record = request.env["omni.automation.log"].sudo().create(
            {
                "trigger": payload.get("trigger", "external_workflow"),
                "action": payload.get("action", "log"),
                "status": payload.get("status", "pending"),
                "payload": json.dumps(payload.get("payload", payload), indent=2),
                "error_message": payload.get("error_message"),
            }
        )
        return self._json_response({"id": record.id, "status": record.status}, 201)

    @http.route("/api/omni/vendor-bill", type="http", auth="public", methods=["POST"], csrf=False)
    def create_vendor_bill(self, **_kwargs):
        """Create a draft vendor bill from structured invoice data."""

        if not self._is_authorized():
            return self._json_response({"error": "Unauthorized"}, 401)

        try:
            payload = self._parse_payload()
        except json.JSONDecodeError:
            return self._json_response({"error": "Invalid JSON payload"}, 400)
        partner_name = payload.get("vendor")
        if not partner_name:
            return self._json_response({"error": "Vendor is required"}, 400)

        partner = request.env["res.partner"].sudo().search([("name", "=", partner_name)], limit=1)
        if not partner:
            partner = request.env["res.partner"].sudo().create({"name": partner_name, "supplier_rank": 1})

        bill = request.env["account.move"].sudo().create(
            {
                "move_type": "in_invoice",
                "partner_id": partner.id,
                "invoice_date": payload.get("date"),
                "ref": f"Imported - {partner_name}",
                "narration": (
                    "Imported by omni-odoo-stack.\n\n"
                    f"Currency: {payload.get('currency', 'USD')}\n"
                    f"Amount: {payload.get('amount', '0')}\n"
                    f"Extracted payload:\n{json.dumps(payload, indent=2)}"
                ),
            }
        )
        body = {"id": bill.id, "name": bill.name, "partner": partner.name}
        return self._json_response(body, 201)

    @http.route("/api/omni/hr/employee", type="http", auth="public", methods=["POST"], csrf=False)
    def create_employee(self, **_kwargs):
        """Create an HR employee record from an onboarding payload."""

        if not self._is_authorized():
            return self._json_response({"error": "Unauthorized"}, 401)

        try:
            payload = self._parse_payload()
        except json.JSONDecodeError:
            return self._json_response({"error": "Invalid JSON payload"}, 400)
        if not payload.get("name"):
            return self._json_response({"error": "Employee name is required"}, 400)
        employee = request.env["hr.employee"].sudo().create(
            {
                "name": payload.get("name"),
                "work_email": payload.get("email"),
                "mobile_phone": payload.get("phone"),
                "job_title": payload.get("job_title"),
            }
        )
        body = {"id": employee.id, "name": employee.name}
        return self._json_response(body, 201)
