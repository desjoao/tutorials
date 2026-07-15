from odoo import api, fields, models
from odoo.exceptions import UserError
from datetime import timedelta


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Offer made for a Property'

    price = fields.Float()
    status = fields.Selection(copy=False, selection=[('accepted', 'Accepted'),('refused', 'Refused')])
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")

    @api.depends("validity", "create_date")
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)


    @api.depends("validity", "create_date")
    def _inverse_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (record.date_deadline - record.create_date.date()).days

    def accept_offer(self):
        for record in self:
            record.status = 'accepted'
        return True

    def refuse_offer(self):
        for record in self:
            record.status = 'refused'
        return True
