
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class PaymentAcquirer(models.Model):
    _inherit = 'payment.acquirer'

    provider = fields.Selection(selection_add=[('cod', 'COD')], default='transfer', ondelete={'cod': 'set default'})

    @api.depends('provider')
    def _compute_view_configuration_fields(self):
        """ Override of payment to hide the credentials page.

        :return: None
        """
        super()._compute_view_configuration_fields()
        self.filtered(lambda acq: acq.provider == 'cod').write({
            'show_credentials_page': False,
            'show_payment_icon_ids': False,
            'show_pre_msg': False,
            'show_done_msg': True,
            'show_cancel_msg': False,
        })

    # @api.constrains('state', 'provider')
    # def _check_acquirer_state(self):
    #     if self.filtered(lambda a: a.provider == 'cod' and a.state not in ('cod', 'disabled')):
    #         raise UserError(_("COD acquirers should never be enabled."))

    def _get_default_payment_method_id(self):
        self.ensure_one()
        print ("=======",self.provider)
        if self.provider != 'cod':
            return super()._get_default_payment_method_id()
        return self.env.ref('payment_cod.payment_method_cod').id
