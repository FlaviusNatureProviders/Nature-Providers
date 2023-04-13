# -*- coding: utf-8 -*-
# from odoo import http


# class SalesInherit(http.Controller):
#     @http.route('/sales_inherit/sales_inherit', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sales_inherit/sales_inherit/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sales_inherit.listing', {
#             'root': '/sales_inherit/sales_inherit',
#             'objects': http.request.env['sales_inherit.sales_inherit'].search([]),
#         })

#     @http.route('/sales_inherit/sales_inherit/objects/<model("sales_inherit.sales_inherit"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sales_inherit.object', {
#             'object': obj
#         })


