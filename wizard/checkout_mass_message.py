from odoo import api, models, fields, exceptions
import logging

_logger = logging.getLogger(__name__)


class CheckoutMassMessage(models.TransientModel):
    _name = "tutorial.library.checkout.massmessage"
    _description = "Send message to Borrowers"

    checkout_ids = fields.Many2many(
        "tutorial.library.checkout", relation="checkout_mm_rel_wz", string="Checkouts"
    )
    message_subject = fields.Char()
    message_body = fields.Html()

    @api.model
    def default_get(self, fields_list):
        defaults_dict = super().default_get(fields_list)
        checkout_ids = self.env.context["active_ids"]
        defaults_dict["checkout_ids"] = [(6, 0, checkout_ids)]
        return defaults_dict

    # self.
    def button_send(self):
        self.ensure_one()
        if not self.checkout_ids:
            raise exceptions.UserError("No Checkouts were select.")

        if not self.message_body:
            raise exceptions.UserError("A message body is required")

        for checkout in self.checkout_ids:
            checkout.message_post(  # type: ignore
                body=self.message_body,
                subject=self.message_subject,
                subtype_xmlid="mail.mt_comment",
            )
            _logger.debug(
                "Message on %d to followers: %s",
                checkout.id,  # type:ignore
                checkout.message_follower_ids,  # type: ignore
            )

        _logger.info(
            "Posted %d messages to the Checkouts: %s",
            len(self.checkout_ids),
            str(self.checkout_ids),
        )

        return True
