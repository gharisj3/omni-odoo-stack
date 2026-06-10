# Purpose: Odoo manifest for the omni_whatsapp integration bridge module.

{
    "name": "Omni WhatsApp",
    "summary": "Meta WhatsApp webhook bridge and message history for CRM.",
    "version": "19.0.1.0.0",
    "category": "Sales/CRM",
    "author": "Muhammad Gharis Javed",
    "website": "https://www.omni-academy.com",
    "license": "LGPL-3",
    "depends": ["crm", "omni_crm"],
    "data": [
        "security/ir.model.access.csv",
        "views/omni_whatsapp_views.xml",
        "data/demo_messages.xml",
    ],
    "installable": True,
    "application": True,
}

