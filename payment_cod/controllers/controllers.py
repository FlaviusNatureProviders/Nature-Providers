# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class PaymentTestController(http.Controller):

    @http.route('/payment/cod/simulate_payment', type='json', auth='public')
    def test_simulate_payment(self, reference, customer_input):
        """ Simulate the response of a payment request.

        :param str reference: The reference of the transaction
        :param str customer_input: The payment method details
        :return: None
        """
        fake_api_response = {
            'reference': reference,
            'cc_summary': customer_input[-4:],
        }
        request.env['payment.transaction'].sudo()._handle_feedback_data('cod', fake_api_response)
