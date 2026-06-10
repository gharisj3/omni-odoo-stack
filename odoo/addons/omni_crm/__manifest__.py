# Purpose: Odoo manifest for the omni_crm custom CRM enhancement module.

{
    "name": "Omni CRM",
    "summary": "Lead scoring, WhatsApp shortcuts, AI summaries, and CRM intake APIs.",
    "version": "19.0.1.0.0",
    "category": "Sales/CRM",
    "author": "Muhammad Gharis Javed",
    "website": "https://www.omni-academy.com",
    "license": "LGPL-3",
    "depends": ["crm"],
    "data": [
        "security/ir.model.access.csv",
        "views/crm_lead_views.xml",
        "data/demo_leads.xml",
    ],
    "demo": ["data/demo_leads.xml"],
    "installable": True,
    "application": True,
}

