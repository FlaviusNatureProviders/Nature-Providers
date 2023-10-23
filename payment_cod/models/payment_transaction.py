
import logging

from odoo import _, api, models
from odoo.exceptions import ValidationError

from odoo.addons.payment import utils as payment_utils

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _send_payment_request(self):
        """ Override of payment to simulate a payment request.

        Note: self.ensure_one()

        :return: None
        """
        print ("======self==========",self)
        super()._send_payment_request()
        if self.provider != 'cod':
            return

        # The payment request response would normally transit through the controller but in the end,
        # all that interests us is the reference. To avoid making a localhost request, we bypass the
        # controller and handle the fake feedback data directly.
        self._handle_feedback_data('cod', {'reference': self.reference})

    @api.model
    def _get_tx_from_feedback_data(self, provider, data):
        """ Override of payment to find the transaction based on dummy data.

        :param str provider: The provider of the acquirer that handled the transaction
        :param dict data: The dummy feedback data
        :return: The transaction if found
        :rtype: recordset of `payment.transaction`
        :raise: ValidationError if the data match no transaction
        """
        tx = super()._get_tx_from_feedback_data(provider, data)
        if provider != 'cod':
            return tx

        reference = data.get('reference')
        tx = self.search([('reference', '=', reference), ('provider', '=', 'cod')])
        if not tx:
            raise ValidationError(
                "COD: " + _("No transaction found matching reference %s.", reference)
            )
        return tx

    def _process_feedback_data(self, data):
        """ Override of payment to process the transaction based on dummy data.

        Note: self.ensure_one()

        :param dict data: The dummy feedback data
        :return: None
        :raise: ValidationError if inconsistent data were received
        """
        super()._process_feedback_data(data)
        if self.provider != "cod":
            return
        print ("Successwwwwwwwwwwwwwwwwwwwwwwww")
        self._set_done()  # Dummy transactions are always successful
        print ("Successddddddddddddddddddddd")
        # if self.tokenize:
        #     token = self.env['payment.token'].create({
        #         'acquirer_id': self.acquirer_id.id,
        #         'name': payment_utils.build_token_name(payment_details_short=data['cc_summary']),
        #         'partner_id': self.partner_id.id,
        #         'acquirer_ref': 'Cash on delivery acquirer reference',
        #         'verified': True,
        #     })
        #     self.token_id = token.id

    def _reconcile_after_done(self):
        
        print ("=-=&&&&&&&&&& inside tx &&&&&&&&")
        result = super(PaymentTransaction,self)._reconcile_after_done()
        return result

    def _create_payment(self, **extra_create_values):
        """Create an `account.payment` record for the current transaction.
        If the transaction is linked to some invoices, their reconciliation is done automatically.

        Note: self.ensure_one()

        :param dict extra_create_values: Optional extra create values
        :return: The created payment
        :rtype: recordset of `account.payment`
        """
        self.ensure_one()

        print ("===============pay123111111111ment created from here===============",self.acquirer_id.name)
        # self.ensure_one()

        if self.acquirer_id.name != 'Cash on delivery':

            payment_method_line = self.acquirer_id.journal_id.inbound_payment_method_line_ids.filtered(lambda l: l.code == self.provider)
            payment_values = {
                'amount': abs(self.amount),  # A tx may have a negative amount, but a payment must >= 0
                'payment_type': 'inbound' if self.amount > 0 else 'outbound',
                'currency_id': self.currency_id.id,
                'partner_id': self.partner_id.commercial_partner_id.id,
                'partner_type': 'customer',
                'journal_id': self.acquirer_id.journal_id.id,
                'company_id': self.acquirer_id.company_id.id,
                'payment_method_line_id': payment_method_line.id,
                'payment_token_id': self.token_id.id,
                'payment_transaction_id': self.id,
                'ref': self.reference,
                **extra_create_values,
            }
            payment = self.env['account.payment'].create(payment_values)
            payment.action_post()

            # Track the payment to make a one2one.
            self.payment_id = payment

            print ("===============payment created from here===============",payment,payment.name)

            if self.invoice_ids:    
                self.invoice_ids.filtered(lambda inv: inv.state == 'draft').action_post()

                (payment.line_ids + self.invoice_ids.line_ids).filtered(
                    lambda line: line.account_id == payment.destination_account_id
                    and not line.reconciled
                ).reconcile()

        return

        # return payment
        # return super(PaymentTransaction, self)._create_payment(**extra_create_values)
