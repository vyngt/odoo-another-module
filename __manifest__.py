# -*- coding: utf-8 -*-
{
    "name": "Tutorial Book Checkout",
    "description": """
        Members can borrow books
    """,
    "author": "vyngt",
    "website": "https://github.com/vyngt",
    "category": "Services/Library",
    "version": "16.0.0.1",
    "depends": ["tutorial_member", "mail"],
    "data": [
        "security/ir.model.access.csv",
        "wizard/checkout_mass_message_wizard_view.xml",
        "views/menu.xml",
        "views/checkout_view.xml",
        "data/stage.xml",
    ],
}
