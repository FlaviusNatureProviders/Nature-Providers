# -*- coding: utf-8 -*-
{
    'name': "SALES INHERIT",
    'author': "IT-PODIUM",
    'category': 'Extra Tools',
    'version': '18.0.0.1',

    'depends': ['base', 'sale'],

    'data': [
        'security/ir.model.access.csv',
        'views/sales_order_inherit_views.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
