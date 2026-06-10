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

    @http.route("/api/omni/automation/log", type="http", auth="public", methods=["POST"], csrf=False)
    def create_log(self, **_kwargs):
        """Store an automation event sent by an external workflow engine."""

        if not self._is_authorized():
            return request.make_response(json.dumps({"error": "Unauthorized"}), headers=[("Content-Type", "application/json")], status=401)

        payload = json.loads(request.httprequest.data.decode("utf-8") or "{}")
        record = request.env["omni.automation.log"].sudo().create(
            {
                "trigger": payload.get("trigger", "external_workflow"),
                "action": payload.get("action", "log"),
                "status": payload.get("status", "pending"),
                "payload": json.dumps(payload.get("payload", payload), indent=2),
                "error_message": payload.get("error_message"),
            }
        )
        return request.make_response(json.dumps({"id": record.id, "status": record.status}), headers=[("Content-Type", "application/json")], status=201)

    @http.route("/api/omni/vendor-bill", type="http", auth="public", methods=["POST"], csrf=False)
    def create_vendor_bill(self, **_kwargs):
        """Create a draft vendor bill from structured invoice data."""

        if not self._is_authorized():
            return request.make_response(json.dumps({"error": "Unauthorized"}), headers=[("Content-Type", "application/json")], status=401)

        payload = json.loads(request.httprequest.data.decode("utf-8") or "{}")
        partner_name = payload.get("vendor")
        if not partner_name:
            return request.make_response(json.dumps({"error": "Vendor is required"}), headers=[("Content-Type", "application/json")], status=400)

        partner = request.env["res.partner"].sudo().search([("name", "=", partner_name)], limit=1)
        if not partner:
            partner = request.env["res.partner"].sudo().create({"name": partner_name, "supplier_rank": 1})

        invoice_lines = []
        for item in payload.get("line_items") or []:
            invoice_lines.append(
                (
                    0,
                    0,
                    {
                        "name": item.get("description") or "Imported line item",
                        "quantity": item.get("quantity", 1),
                        "price_unit": item.get("unit_price", item.get("total", 0)),
                    },
                )
            )

        bill = request.env["account.move"].sudo().create(
            {
                "move_type": "in_invoice",
                "partner_id": partner.id,
                "invoice_date": payload.get("date"),
                "ref": f"Imported - {partner_name}",
                "invoice_line_ids": invoice_lines,
                "narration": f"Imported by omni-odoo-stack with currency {payload.get('currency', 'USD')}.",
            }
        )
        body = {"id": bill.id, "name": bill.name, "partner": partner.name}
        return request.make_response(json.dumps(body), headers=[("Content-Type", "application/json")], status=201)

    @http.route("/api/omni/hr/employee", type="http", auth="public", methods=["POST"], csrf=False)
    def create_employee(self, **_kwargs):
        """Create an HR employee record from an onboarding payload."""

        if not self._is_authorized():
            return request.make_response(json.dumps({"error": "Unauthorized"}), headers=[("Content-Type", "application/json")], status=401)

        payload = json.loads(request.httprequest.data.decode("utf-8") or "{}")
        employee = request.env["hr.employee"].sudo().create(
            {
                "name": payload.get("name"),
                "work_email": payload.get("email"),
                "mobile_phone": payload.get("phone"),
                "job_title": payload.get("job_title"),
            }
        )
        body = {"id": employee.id, "name": employee.name}
        return request.make_response(json.dumps(body), headers=[("Content-Type", "application/json")], status=201)
