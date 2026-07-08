from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Definition of types of the Real Estate properties'

    name = fields.Char(required=True)
