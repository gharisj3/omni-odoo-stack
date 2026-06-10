"""Purpose: Persist inbound and outbound WhatsApp messages tied to CRM leads."""

from __future__ import annotations

from odoo import api, fields, models


class OmniWhatsappMessage(models.Model):
    """Message log for Meta WhatsApp conversations linked to leads."""

    _name = "omni.whatsapp.message"
    _description = "Omni WhatsApp Message"
    _order = "create_date desc"

    phone = fields.Char(required=True)
    message = fields.Text(required=True)
    direction = fields.Selection([("in", "Incoming"), ("out", "Outgoing")], required=True, default="in")
    status = fields.Selection(
        [("received", "Received"), ("processed", "Processed"), ("sent", "Sent"), ("failed", "Failed")],
        default="received",
        required=True,
    )
    lead_id = fields.Many2one("crm.lead", string="Lead", ondelete="set null")
    external_message_id = fields.Char(string="External Message ID")
    payload = fields.Text(string="Payload JSON")
    name = fields.Char(compute="_compute_name", store=True)

    @api.depends("phone", "direction", "create_date")
    def _compute_name(self) -> None:
        """Build a readable record name."""

        for record in self:
            record.name = f"{record.phone or 'Unknown'} [{record.direction or 'n/a'}]"

