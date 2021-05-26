# -*- coding: utf-8 -*-
{
    'name': "hr_request",

    'summary': """This Module Add Many Customized HR Screens, And Add Customized Setting Screen""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Ahmed Saber",
    'website': "http://www.marketme-it.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'hr_employee_updation', 'hr_contract'],

    # always loaded
    'data': [
        'security/hr_security_group.xml',
        'security/ir.model.access.csv',
        'views/late_permission.xml',
        'views/disclaimer.xml',
        'views/settings.xml',
        'data/emails.xml',
        'data/sequence.xml',
        'data/contract_cron.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
