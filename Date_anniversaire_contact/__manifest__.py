# -*- coding: utf-8 -*-
{
    'name': "Date_anniversaire_contact",

    'summary': """
         Visualiser les dates d'anniversaire des contacts""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Nadia",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Gestion de l\'école ',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'bibliotheque'],

    # always loaded
    'data': [
        'views/res_partner.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}