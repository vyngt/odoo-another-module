from odoo import models, fields


class CheckoutStage(models.Model):
    _name = "tutorial.library.checkout.stage"
    _description = "Checkout Stages"
    _order = "sequence"

    name = fields.Char()
    sequence = fields.Integer(default=10)
    fold = fields.Boolean()
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [
            ("new", "Requested"),
            ("open", "Borrowed"),
            ("done", "Returned"),
            ("cancel", "Canceled"),
        ],
        default="new",
    )
