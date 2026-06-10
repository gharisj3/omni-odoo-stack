"""Purpose: Log AI requests and orchestrate lead analysis via the FastAPI middleware."""

from __future__ import annotations

import json
import logging
import os

import requests

from odoo import _, api, fields, models
from odoo.exceptions import UserError

LOGGER = logging.getLogger(__name__)


class OmniAIRequest(models.Model):
    """AI request log and bridge for CRM lead analysis."""

    _name = "omni.ai.request"
    _description = "Omni AI Request"
    _order = "create_date desc"

    prompt = fields.Text(required=True)
    response = fields.Text()
    model_used = fields.Char(default="llama3-8b-8192", required=True)
    tokens_used = fields.Integer(default=0)
    status = fields.Selection(
        [("pending", "Pending"), ("success", "Success"), ("failed", "Failed")],
        default="pending",
        required=True,
    )
    lead_id = fields.Many2one("crm.lead", string="Lead", ondelete="cascade")
    created_at = fields.Datetime(default=fields.Datetime.now, readonly=True)
    error_message = fields.Text()

    @api.model
    def _middleware_endpoint(self, path: str) -> str:
        """Build a fully qualified middleware URL."""

        base_url = os.getenv("OMNI_AI_ENDPOINT", "http://ai-middleware:8000").rstrip("/")
        return f"{base_url}{path}"

    @api.model
    def _api_headers(self) -> dict[str, str]:
        """Return authenticated headers for the shared middleware."""

        api_key = os.getenv("AI_SHARED_API_KEY")
        if not api_key:
            raise UserError(_("AI_SHARED_API_KEY is not configured for Odoo."))
        return {"X-API-Key": api_key, "Content-Type": "application/json"}

    @api.model
    def process_lead(self, lead_id: int) -> "OmniAIRequest":
        """Send a lead to the middleware, store the response, and update the lead."""

        lead = self.env["crm.lead"].browse(lead_id).exists()
        if not lead:
            raise UserError(_("Lead not found for AI processing."))

        prompt_payload = {
            "name": lead.name,
            "email": lead.email_from,
            "phone": lead.phone,
            "description": lead.description or "",
            "company": lead.partner_name,
        }
        request_log = self.create(
            {
                "lead_id": lead.id,
                "prompt": json.dumps(prompt_payload, indent=2),
                "status": "pending",
            }
        )
        try:
            response = requests.post(
                self._middleware_endpoint("/analyze/lead"),
                headers=self._api_headers(),
                data=json.dumps(prompt_payload),
                timeout=30,
            )
            response.raise_for_status()
            payload = response.json()
            request_log.write(
                {
                    "response": json.dumps(payload, indent=2),
                    "tokens_used": int(payload.get("_usage", {}).get("total_tokens", 0)),
                    "status": "success",
                }
            )
            lead.write(
                {
                    "omni_ai_analysis": payload.get("summary"),
                    "omni_priority": payload.get("priority", "medium"),
                    "omni_last_analysis_at": fields.Datetime.now(),
                }
            )
        except Exception as exc:  # pylint: disable=broad-except
            LOGGER.exception("Lead AI processing failed")
            request_log.write({"status": "failed", "error_message": str(exc)})
        return request_log

    @api.model
    def cron_process_unanalyzed_leads(self) -> None:
        """Find candidate leads that still need an AI summary and process them."""

        leads = self.env["crm.lead"].search([("omni_ai_analysis", "=", False)], limit=20)
        for lead in leads:
            self.process_lead(lead.id)
