# Purpose: Odoo manifest for the omni_automation orchestration module.

{
    "name": "Omni Automation",
    "summary": "Pipeline orchestration and automation observability for the omni stack.",
    "version": "19.0.1.0.0",
    "category": "Operations",
    "author": "Muhammad Gharis Javed",
    "website": "https://www.omni-academy.com",
    "license": "LGPL-3",
    "depends": ["crm", "account", "hr", "omni_crm", "omni_whatsapp", "omni_ai"],
    "data": [
        "security/ir.model.access.csv",
        "views/omni_automation_views.xml",
        "data/demo_logs.xml",
    ],
    "installable": True,
    "application": True,
}
