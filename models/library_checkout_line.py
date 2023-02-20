from odoo import models, fields


class CheckoutLine(models.Model):
    _name = "tutorial.library.checkout.line"
    _description = "Checkout Request Line"

    checkout_id = fields.Many2one("tutorial.library.checkout", required=True)
    book_id = fields.Many2one("tutorial.library.book", required=True)
    book_cover = fields.Binary(related="book_id.image")

    note = fields.Char("Notes")
