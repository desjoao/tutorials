# -*- coding: utf-8 -*-

{
    'name': "Real Estate",
    'depends': ['base'],
    'application': True,
    'data': [
        #Security
        'security/ir.model.access.csv',
            
        #Views
        'views/estate_property_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_offers_views.xml',
        'views/estate_menus.xml',
        ],  
}
