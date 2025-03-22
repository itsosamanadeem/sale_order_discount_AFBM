from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)

class DiscountSaleOrder(models.Model):
    _name = "discount.sale.order"

    name = fields.Char(string="Miscellaneous Charge")
    discount = fields.Float(string="Charge")
    
    def unlink(self):
        for record in self:
            product = self.env['product.product'].search([('name', '=', record.name)], limit=1)
            if product:
                product.unlink()  
        return super(DiscountSaleOrder, self).unlink()
