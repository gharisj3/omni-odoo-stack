# Purpose: Odoo manifest for the omni_ai middleware bridge module.

{
    "name": "Omni AI",
    "summary": "AI request logging and lead analysis bridge for Groq-backed middleware.",
    "version": "19.0.1.0.0",
    "category": "Technical",
    "author": "Muhammad Gharis Javed",
    "website": "https://www.omni-academy.com",
    "license": "LGPL-3",
    "depends": ["crm", "omni_crm"],
    "data": [
        "security/ir.model.access.csv",
        "views/omni_ai_views.xml",
        "data/cron.xml",
        "data/demo_ai_requests.xml",
    ],
    "installable": True,
    "application": True,
}

