# -*- coding: utf-8 -*-
{
    'name': "Amirah",

    'summary': """ Amirah """,

    'description': """
        Amirah
    """,

    'author': "aquíH",
    'website': "http://www.aquih.com",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['website','base','stock', 'theme_prime', 'sale'],

    'data': [
        'data/amirah_data.xml',
        'data/paper_format.xml',
        'views/formato_etiquetas.xml',
        'wizard/reporte_inventario.xml',
        'wizard/reporte_ventas.xml',
        'security/ir.model.access.csv',
        'views/templates.xml',
    ],

    'qweb': [
    ],
}
