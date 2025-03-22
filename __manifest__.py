{
    'name': 'Sale Order Line Inherit',
    'summary': 'Manage and organize employee working schedules.',
    'author': 'Osama Nadeem',
    'sequence': '-100',
    'license': 'LGPL-3',
    'depends': ['base', 'sale', 'product','purchase','sale_order_type'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/select_discount_wizard.xml',
        'views/discount_record.xml',
        'views/sale_order_line.xml',
        'views/product_discount_price.xml',
        # 'views/purchase_requisation_view_inherit.xml'
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': True,
}
