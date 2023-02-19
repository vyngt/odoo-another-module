from odoo import models, fields, api, exceptions


class LibraryCheckout(models.Model):
    _name = "tutorial.library.checkout"
    _description = "Checkout Request"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Title")
    member_id = fields.Many2one("res.users", required=True)
    member_image = fields.Image(related="member_id.image_128")
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

    count_checkouts = fields.Integer(compute="_compute_count_checkouts")
    num_books = fields.Integer(compute="_compute_num_books", store=True)

    @api.depends("line_ids")
    def _compute_num_books(self):
        for checkout in self:
            checkout.num_books = len(checkout.line_ids)

    def _compute_count_checkouts(self):
        members = self.mapped("member_id")
        domain = [
            ("member_id", "in", members.ids),  # type: ignore
            ("state", "not in", ["done", "cancel"]),
        ]
        raw = self.read_group(domain, ["id:count"], ["member_id"])
        data = {x["member_id"][0]: x["member_id_count"] for x in raw}

        for checkout in self:
            checkout.count_checkouts = data.get(checkout.member_id.id, 0)  # type: ignore

    @api.model
    def _default_stage_id(self):
        Stage = self.env["tutorial.library.checkout.stage"]
        stage = Stage.search([("state", "=", "new")], limit=1)
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

    def button_done(self):
        Stage = self.env["tutorial.library.checkout.state"]
        done_stage = Stage.search([("state", "=", "done")], limit=1)
        for checkout in self:
            checkout.stage_id = done_stage
        return True
