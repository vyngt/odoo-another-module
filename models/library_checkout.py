from odoo import models, fields, api, exceptions


class LibraryCheckout(models.Model):
    _name = "tutorial.library.checkout"
    _description = "Checkout Request"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    member_id = fields.Many2one("res.users", required=True)
    user_id = fields.Many2one(
        "tutorial.library.member", "Librarian", default=lambda s: s.env.user
    )
    request_date = fields.Date(
        default=lambda s: fields.Date.today(),
        compute="_compute_request_date_onchange",
        store=True,
        readonly=False,
    )

    line_ids = fields.One2many(
        "tutorial.library.checkout.line", "checkout_id", string="Borrowed Books"
    )

    @api.model
    def _default_stage_id(self):
        Stage = self.env["tutorial.library.checkout.stage"]
        stage = Stage.search([("name", "=", "new")], limit=1)
        return stage

    @api.model
    def _group_expand_stage_id(self, stages, domain, order):
        return stages.search([], order=order)

    stage_id = fields.Many2many(
        "tutorial.library.checkout.stage",
        relation="checkout_stage_rel",
        default=_default_stage_id,
        group_expand="_group_expand_stage_id",
    )
    state = fields.Selection(related="stage_id.state")

    checkout_date = fields.Date(readonly=True)
    close_date = fields.Date(readonly=True)

    # Extending create
    @api.model
    def create(self, vals_list):
        new_record = super().create(vals_list)
        if new_record.stage_id.state in ("open", "done"):  # type: ignore
            raise exceptions.UserError("State not allowed for new checkouts.")
        return new_record

    def write(self, vals):
        """Example code -> avoid infinite loop"""

        old_state = self.stage_id.state  # type: ignore
        super().write(vals)
        new_state = self.stage_id.state  # type: ignore

        if not self.env.context.get("_checkout_write"):
            if new_state != old_state:
                if new_state == "open":
                    self.with_context({"_checkout_write": True}).write(
                        {"checkout_date": fields.Date.today()}
                    )
                elif new_state == "done":
                    self.with_context({"_checkout_write": True}).write(
                        {"close_date": fields.Date.today()}
                    )

        return True

    @api.depends("member_id")
    def _compute_request_date_onchange(self):
        today = fields.Date.today()
        if self.request_date != today:
            self.request_date = today
            return {
                "warning": {
                    "title": "Changed request date",
                    "message": "la la la lala",
                }
            }
