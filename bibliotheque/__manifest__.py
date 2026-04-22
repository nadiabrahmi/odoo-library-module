# -*- coding: utf-8 -*-
{
    'name': "Bibliothèque",

    'summary': """
        Gérez votre bibliothèque """,

    'description': """
        Long description of module's purpose
    """,

    'author': "Nadia",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Gestion de la bibliothèque ',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'views/livre_views.xml',
        'views/emprunte_views.xml',
        'views/etiquette_views.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'report/bibliotheque_card.xml',
        'report/report_bibliotheque.xml',
        'report/qr_code_livre_card.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}