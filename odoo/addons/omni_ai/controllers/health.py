"""Purpose: Provide a simple Odoo-level health endpoint for the omni_ai module."""

from __future__ import annotations

import json

from odoo import http
from odoo.http import request


class OmniAIController(http.Controller):
    """Small health helper for Odoo module visibility."""

    @http.route("/api/omni/ai/health", type="http", auth="user", methods=["GET"])
    def ai_health(self, **_kwargs):
        """Return module health details from inside Odoo."""

        body = json.dumps({"status": "ok", "model": "omni.ai.request"})
        return request.make_response(body, headers=[("Content-Type", "application/json")], status=200)

