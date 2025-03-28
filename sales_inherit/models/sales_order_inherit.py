# -*- coding: utf-8 -*-

from odoo import fields, models, api, _

from collections import defaultdict
from odoo.tools import float_is_zero


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def sale_product_view_inherit(self):
        stock_id = self.env['sale.order.product.list']
        product_id = self.env['product.product']

        stock_product_move_id = self.env['sale.order.line'].search([('order_id.partner_id', '=', self.partner_id.id)])
        product_move_list = stock_id.search([('partner_id', '=', self.partner_id.id)])

        product_move_history_list = [st_id.product_id.id for st_id in stock_product_move_id]
        stock_product_list = [pt_id.product_id.id for pt_id in product_move_list]

        list_difference = [item for item in product_move_history_list if item not in stock_product_list]

        if list_difference:
            stock_move_list = product_id.search([('id', 'in', list_difference)])
            for products in stock_move_list:
                stock_id.create({'name': products.name, 'product_id': products.id, 'partner_id': self.partner_id.id,
                                 'product_image': products.product_tmpl_id.image_1920})

        kanban = self.env.ref('sales_inherit.view_order_inherit_kanban', False)
        tree = self.env.ref('sales_inherit.view_order_inherit_tree', False)
        form = self.env.ref('sales_inherit.view_order_inherit_form', False)

        return {
            'name': 'Product view',
            'type': 'ir.actions.act_window',
            'view_type': 'kanban',
            'view_mode': 'kanban,list,form',
            'views': [(kanban.id, 'kanban'), (tree.id, 'list'), (form.id, 'form')],
            'res_model': 'sale.order.product.list',
            'target': 'current',
            'domain': [('partner_id', '=', self.partner_id.id), ('product_id.active', '=', True)],
            'context': {
                'default_partner_id': self.partner_id.id,
                'sale_order': self.id
            },
        }


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    image_product = fields.Binary('Images', related='product_template_id.image_1920')


class SaleOrderProductList(models.Model):
    _name = "sale.order.product.list"
    _description = "Sale Order Product List"

    name = fields.Char(string='Name')
    product_id = fields.Many2one('product.product', string="Product Name")
    stock_view_ids = fields.One2many('stock.product.list', 'stock_view_id', string='Product Order Lines')
    sale_order_id = fields.Many2one('sale.order', string="Sales Order")
    partner_id = fields.Many2one('res.partner', string="Customer")
    product_image = fields.Binary(string='Product image', related='product_id.product_tmpl_id.image_1920')
    product_count = fields.Integer(string="Count", readonly=False)
    categ_id = fields.Many2one('product.category', related='product_id.product_tmpl_id.categ_id', store=True)

    def add_to_sales_order(self):
        order_id = self.env.context.get('sale_order')
        line_env = self.env['sale.order.line']
        if self.product_count != 0:
            new_line = line_env.create({
                'product_id': self.product_id.id,
                'order_id': order_id,
                'product_uom_qty': self.product_count
            })
            # new_line.product_id_change()
            # new_line._onchange_discount()
            self.product_count = 0

    def add_quantity_manually(self):
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('sales_inherit.product_quantity_popup').id,
            'res_model': 'sale.order.product.list',
            'target': 'new',
            'res_id': self.id,
        }

    def action_close(self):
        return {
            'type': 'ir.actions.act_window_close'
        }

    def add_product(self):
        self.product_count = self.product_count + 1

    def remove_product(self):
        if self.product_count != 0:
            self.product_count = self.product_count - 1

    def add_products(self):
        line_env = self.env['sale.order.line']
        order_id = self.env.context.get('sale_order')
        if order_id:
            for values in self:
                new_line = line_env.create({
                    'product_id': values.product_id.id,
                    'order_id': order_id
                })
                # new_line.product_id_change()
                # new_line._onchange_discount()
            form_id = self.env.ref('sale.view_order_form', False)
            tree_id = self.env.ref('sale.view_order_tree', False)

            return {
                'view_type': 'form',
                'view_mode': 'form,list',
                'res_model': 'sale.order',
                'res_id': order_id,
                'view_id': False,
                'views': [(form_id.id, 'form'), (tree_id.id, 'list')],
                'type': 'ir.actions.act_window',
            }
        else:
            raise ValidationError(_("Your quotation contains products from company"))


class StockProductList(models.Model):
    _name = "stock.product.list"
    _description = "Stock Product List"

    name = fields.Char(string='Name')
    product_id = fields.Many2one('product.product', string="Product Name")
    stock_view_id = fields.Many2one('sale.order.product.list', string="Product Stock Name")
    select = fields.Boolean(string="Select")
