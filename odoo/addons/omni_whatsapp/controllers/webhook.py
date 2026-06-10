"""Purpose: Receive and verify Meta WhatsApp webhook traffic."""

from __future__ import annotations

import json
import os

from odoo import http
from odoo.http import request


class OmniWhatsappWebhookController(http.Controller):
    """Meta webhook endpoints for inbound WhatsApp messages."""

    @http.route("/whatsapp/webhook", type="http", auth="public", methods=["GET"], csrf=False)
    def verify_webhook(self, **kwargs):
        """Handle Meta verification challenges during webhook setup."""

        mode = kwargs.get("hub.mode")
        token = kwargs.get("hub.verify_token")
        challenge = kwargs.get("hub.challenge")
        if mode == "subscribe" and token == os.getenv("META_VERIFY_TOKEN"):
            return request.make_response(challenge or "", headers=[("Content-Type", "text/plain")], status=200)
        return request.make_response("Verification failed", headers=[("Content-Type", "text/plain")], status=403)

    @http.route("/whatsapp/webhook", type="http", auth="public", methods=["POST"], csrf=False)
    def receive_webhook(self, **_kwargs):
        """Persist inbound WhatsApp events and trigger automation when available."""

        payload = json.loads(request.httprequest.data.decode("utf-8") or "{}")
        messages = payload.get("entry", [{}])[0].get("changes", [{}])[0].get("value", {}).get("messages", [])
        contacts = payload.get("entry", [{}])[0].get("changes", [{}])[0].get("value", {}).get("contacts", [])
        lead_model = request.env["crm.lead"].sudo()
        message_model = request.env["omni.whatsapp.message"].sudo()
        automation_model = request.env["omni.automation.log"].sudo() if "omni.automation.log" in request.env else None

        for index, message in enumerate(messages):
            phone = message.get("from")
            text = message.get("text", {}).get("body", "")
            contact_name = contacts[index].get("profile", {}).get("name") if index < len(contacts) else phone
            lead = lead_model.search([("phone", "ilike", phone)], limit=1)
            if not lead:
                lead = lead_model.create({"name": contact_name or phone, "phone": phone, "description": text})

            record = message_model.create(
                {
                    "phone": phone,
                    "message": text,
                    "direction": "in",
                    "status": "received",
                    "lead_id": lead.id,
                    "external_message_id": message.get("id"),
                    "payload": json.dumps(message),
                }
            )
            if automation_model:
                automation_model.run_whatsapp_pipeline(record.id)

        return request.make_response(json.dumps({"status": "accepted"}), headers=[("Content-Type", "application/json")], status=200)

