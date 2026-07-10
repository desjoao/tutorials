from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Definition of tags for the Real Estate properties'

    name = fields.Char(required=True)

