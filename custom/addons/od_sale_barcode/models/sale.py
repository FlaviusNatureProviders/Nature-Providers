# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = ['sale.order', 'barcodes.barcode_events_mixin']

    def on_barcode_scanned(self, barcode):
        if barcode:
            product_env = self.env['product.product']
            product = product_env.search([('barcode', '=', barcode)], limit=1)
            if product:
                sale_line = self.order_line.filtered(lambda r: r.product_id.id == product.id)
                if sale_line:
                    sale_line.update({'product_uom_qty': sale_line.product_uom_qty + 1})
                else:
                    sequence = max(self.order_line.mapped('sequence')) if self.order_line.mapped('sequence') else 10
                    vals = {
                        'product_id': product.id,
                        'order_id': self.id,
                        'product_uom_qty': 1,
                        'sequence': sequence + 1,
                    }
                    order_line = self.order_line.new(vals)
                    # order_line.product_id_change()
            else:
                raise UserError(_('Invalid Barcode %s Scanned!' % barcode))
