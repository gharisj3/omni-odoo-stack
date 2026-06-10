"""Purpose: Expose CRM lead intake endpoints for external automation tools."""

from __future__ import annotations

import json
import os

from odoo import http
from odoo.http import request


class OmniLeadAPIController(http.Controller):
    """JSON API controller for CRM lead creation."""

    def _authorize(self) -> bool:
        """Validate the shared API key configured for the omni stack."""

        expected_key = os.getenv("OMNI_API_KEY")
        received_key = request.httprequest.headers.get("X-Omni-API-Key")
        return bool(expected_key and received_key and expected_key == received_key)

    @staticmethod
    def _json_response(payload: dict, status_code: int):
        """Return a JSON response with a consistent content type."""

        return request.make_response(
            json.dumps(payload),
            headers=[("Content-Type", "application/json")],
            status=status_code,
        )

    @http.route("/api/omni/lead", type="http", auth="public", methods=["POST"], csrf=False)
    def create_lead(self, **_kwargs):
        """Create a CRM lead from a JSON payload sent by an external system."""

        if not self._authorize():
            return self._json_response({"error": "Unauthorized"}, 401)

        try:
            payload = json.loads(request.httprequest.data.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            return self._json_response({"error": "Invalid JSON payload"}, 400)
        lead = request.env["crm.lead"].sudo().create_from_api(payload)
        response = {
            "id": lead.id,
            "name": lead.name,
            "score": lead.omni_lead_score,
            "priority": lead.omni_priority,
        }
        return self._json_response(response, 201)
