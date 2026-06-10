"""Purpose: Extend CRM leads with AI scoring, summaries, and WhatsApp actions."""

from __future__ import annotations

import os

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class CrmLead(models.Model):
    """Enhance crm.lead with scoring and lightweight AI workflow hooks."""

    _inherit = "crm.lead"
    _description = "CRM Lead with Omni Enhancements"

    omni_lead_score = fields.Integer(
        string="Lead Score",
        compute="_compute_omni_lead_score",
        store=True,
        help="Computed lead qualification score from 1 to 10.",
    )
    omni_ai_analysis = fields.Text(
        string="AI Analysis",
        help="Latest AI-generated lead summary and next-step guidance.",
    )
    omni_priority = fields.Selection(
        [
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High"),
            ("urgent", "Urgent"),
        ],
        string="AI Priority",
        default="medium",
    )
    omni_last_analysis_at = fields.Datetime(string="Last AI Analysis At", readonly=True)
    omni_whatsapp_url = fields.Char(
        string="WhatsApp URL",
        compute="_compute_omni_whatsapp_url",
        help="Convenience deep link for starting a WhatsApp chat with the lead.",
    )
    color = fields.Integer(string="Kanban Color", compute="_compute_color", store=True)

    @api.depends("name", "email_from", "phone", "expected_revenue", "description", "probability")
    def _compute_omni_lead_score(self) -> None:
        """Compute a simple but transparent lead score for demos and automation."""

        for lead in self:
            score = 1
            if lead.email_from:
                score += 2
            if lead.phone:
                score += 2
            if lead.description and len(lead.description.strip()) > 40:
                score += 2
            if lead.expected_revenue and lead.expected_revenue >= 1000:
                score += 2
            if lead.probability and lead.probability >= 50:
                score += 1
            lead.omni_lead_score = min(score, 10)

    @api.depends("phone")
    def _compute_omni_whatsapp_url(self) -> None:
        """Build a direct WhatsApp link from the lead phone number."""

        for lead in self:
            digits = "".join(ch for ch in (lead.phone or "") if ch.isdigit())
            lead.omni_whatsapp_url = f"https://wa.me/{digits}" if digits else False

    @api.depends("omni_lead_score")
    def _compute_color(self) -> None:
        """Color code kanban cards by lead score."""

        for lead in self:
            if lead.omni_lead_score >= 8:
                lead.color = 10
            elif lead.omni_lead_score >= 5:
                lead.color = 2
            else:
                lead.color = 1

    def action_open_whatsapp_chat(self) -> dict:
        """Open the lead's WhatsApp chat in a new browser tab."""

        self.ensure_one()
        if not self.omni_whatsapp_url:
            raise UserError(_("Add a phone number before opening WhatsApp chat."))
        return {"type": "ir.actions.act_url", "url": self.omni_whatsapp_url, "target": "new"}

    def action_run_ai_analysis(self) -> bool:
        """Trigger the AI request model when the omni_ai module is installed."""

        if "omni.ai.request" not in self.env:
            raise UserError(_("Install omni_ai to run lead analysis from Odoo."))
        request_model = self.env["omni.ai.request"]
        for lead in self:
            request_model.process_lead(lead.id)
        return True

    @api.model
    def create_from_api(self, payload: dict) -> "CrmLead":
        """Create a lead record from an external JSON payload."""

        values = {
            "name": payload.get("name"),
            "partner_name": payload.get("company"),
            "email_from": payload.get("email"),
            "phone": payload.get("phone"),
            "description": payload.get("description"),
            "expected_revenue": payload.get("expected_revenue", 0),
        }
        if not values["name"]:
            raise UserError(_("Lead name is required."))
        lead = self.create(values)
        if os.getenv("OMNI_AI_BASE_URL") and "omni.ai.request" in self.env:
            self.env["omni.ai.request"].sudo().process_lead(lead.id)
        return lead
