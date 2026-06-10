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

    @http.route("/api/omni/lead", type="http", auth="public", methods=["POST"], csrf=False)
    def create_lead(self, **_kwargs):
        """Create a CRM lead from a JSON payload sent by an external system."""

        if not self._authorize():
            body = json.dumps({"error": "Unauthorized"})
            return request.make_response(body, headers=[("Content-Type", "application/json")], status=401)

        payload = json.loads(request.httprequest.data.decode("utf-8") or "{}")
        lead = request.env["crm.lead"].sudo().create_from_api(payload)
        response = {
            "id": lead.id,
            "name": lead.name,
            "score": lead.omni_lead_score,
            "priority": lead.omni_priority,
        }
        return request.make_response(
            json.dumps(response),
            headers=[("Content-Type", "application/json")],
            status=201,
        )

