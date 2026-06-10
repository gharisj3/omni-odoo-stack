"""Purpose: Track automation events and connect WhatsApp, CRM, and AI processing."""

from __future__ import annotations

import json

from odoo import api, fields, models


class OmniAutomationLog(models.Model):
    """Central automation log for pipeline events across the stack."""

    _name = "omni.automation.log"
    _description = "Omni Automation Log"
    _order = "create_date desc"

    trigger = fields.Char(required=True)
    action = fields.Char(required=True)
    status = fields.Selection(
        [("pending", "Pending"), ("success", "Success"), ("failed", "Failed")],
        default="pending",
        required=True,
    )
    payload = fields.Text()
    error_message = fields.Text()
    created_at = fields.Datetime(default=fields.Datetime.now, readonly=True)
    lead_id = fields.Many2one("crm.lead", string="Lead", ondelete="set null")
    message_id = fields.Many2one("omni.whatsapp.message", string="WhatsApp Message", ondelete="set null")
    name = fields.Char(compute="_compute_name", store=True)

    @api.depends("trigger", "action", "status")
    def _compute_name(self) -> None:
        """Build a compact human-readable log name."""

        for record in self:
            record.name = f"{record.trigger or 'Automation'} -> {record.action or 'Action'} [{record.status}]"

    @api.model
    def run_whatsapp_pipeline(self, message_id: int) -> "OmniAutomationLog":
        """Process a WhatsApp message into CRM and AI steps with end-to-end logging."""

        message = self.env["omni.whatsapp.message"].browse(message_id).exists()
        payload = {}
        if message:
            payload = {
                "phone": message.phone,
                "message": message.message,
                "lead_id": message.lead_id.id,
            }
        log = self.create(
            {
                "trigger": "whatsapp_webhook",
                "action": "crm_to_ai_pipeline",
                "status": "pending",
                "payload": json.dumps(payload, indent=2),
                "lead_id": message.lead_id.id if message and message.lead_id else False,
                "message_id": message.id if message else False,
            }
        )
        try:
            if message and message.lead_id:
                self.env["omni.ai.request"].sudo().process_lead(message.lead_id.id)
                message.write({"status": "processed"})
            log.write({"status": "success"})
        except Exception as exc:  # pylint: disable=broad-except
            log.write({"status": "failed", "error_message": str(exc)})
            if message:
                message.write({"status": "failed"})
        return log

