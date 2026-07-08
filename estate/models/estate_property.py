from odoo import fields, models
from datetime import datetime
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Properties for the Real Estate Model'

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, 
                                    default= lambda self: datetime.today() + relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
            string='Garden Orientation',
            selection=[('north', 'North'), ('west', 'West'), ('south', 'South'), ('east', 'East')],
            help="Garden Orientation is used to indicate the orientation of the property's garden.")
    active = fields.Boolean(default=True)
    state = fields.Selection(
            string='State',
            selection=[('new', 'New'), ('offer received', 'Offer Received'),
                       ('offer accepted', 'Offer Accepted'), ('sold', 'Sold'),
                       ('cancelled', 'Cancelled')],
            help="Possible states for an indexed property.",
            required=True,
            default='new')
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    salesman_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.uid)
    buyers_id = fields.Many2one("res.partner", string="Buyer", copy=False)

