from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)


class ProductPricingList(models.Model):
    _inherit = 'product.pricelist.item'

    fixed_discount= fields.Float(string="Fixed Discount")
    min_fix_disc= fields.Float(string="Min fix discount")
    max_fix_disc= fields.Float(string="Max fix discount")


    min_perce_disc= fields.Float(string="Min percent discount")
    max_perce_disc= fields.Float(string="Max percent discount")

    @api.onchange('compute_price')
    def onchange_fixed_discount(self):
        # pass
        if self.compute_price != 'formula':
            self.fixed_discount= 0.0
