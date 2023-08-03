# -*- coding: utf-8 -*-
{
    'name': "Cash on delivery",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    'category': 'Hidden',
    'version': '0.1',

    'depends': ['payment','website_sale'],
    'data': [
        'views/payment_token.xml',
        'views/payment_cod_template.xml',
        'data/payment_acquirer_data.xml',
    ],
    'uninstall_hook': 'uninstall_hook',
    'assets': {
        'web.assets_frontend': [
            'payment_cod/static/src/js/**/*',
        ],
    },
}
