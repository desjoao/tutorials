from odoo import api, fields, models
from odoo.exceptions import UserError
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
    selling_price = fields.Float(readonly=True, copy=False, compute="_compute_accepted_price")
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
                       ('canceled', 'Canceled')],
            help="Possible states for an indexed property.",
            required=True,
            default='new')
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    salesman_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.uid)
    buyers_id = fields.Many2one("res.partner", string="Buyer", copy=False, compute='_compute_property_buyer')
    property_tag_ids = fields.Many2many("estate.property.tag", string="Tag")
    property_offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("property_offer_ids")
    def _compute_best_price(self):
        for record in self:
            if record.property_offer_ids:
                best_prices = record.property_offer_ids.mapped('price')
                record.best_price = max(best_prices)
            else:
                record.best_price = None

    @api.depends("property_offer_ids.status", "property_offer_ids.price")
    def _compute_accepted_price(self):
        for record in self:
            accepted_offer = record.property_offer_ids.filtered(lambda o: o.status == 'accepted')
            if accepted_offer:
                record.selling_price = accepted_offer[0].price
            else:
                record.selling_price = 0.0  

    @api.depends("property_offer_ids.status", "property_offer_ids.partner_id")
    def _compute_property_buyer(self):
        for record in self:
            if record.property_offer_ids:
                accepted_offer = record.property_offer_ids.filtered(lambda o: o.status == 'accepted')
                if accepted_offer:
                    record.buyers_id = accepted_offer[0].partner_id
                else:
                    record.buyers_id = None

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = None
            self.garden_orientation = None

    def property_sold(self):
        for record in self:
            if record.state == "canceled":
                raise UserError("Canceled properties cannot be sold.")
            record.state = "sold"
        return True

    def property_canceled(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold properties cannot be canceled.")
            record.state = "canceled"
        return True
