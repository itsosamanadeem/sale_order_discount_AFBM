from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)

class SaleOrderSelectionDiscount(models.TransientModel):
    _name = "sale.order.selection.discount"
    _description = "Miscellaneous Charge Selection Wizard"

    sale_order_id = fields.Many2one("sale.order", string="Sale Order", required=True, readonly=True)
    discount_id = fields.Many2one("discount.sale.order", string="Miscellaneous Charges", required=True)

    def apply_discount(self):
        for rec in self:
            if not rec.discount_id.discount:
                raise ValidationError("Add Discount First Before Applying")

            sale_order = rec.sale_order_id

            discount_product = self.env['product.product'].search([('name', '=', rec.discount_id.name)], limit=1)
            if not discount_product:
                discount_product = self.env['product.product'].create({
                    'name': rec.discount_id.name,
                    'type': 'service',
                    'invoice_policy': 'order',
                    'list_price': 0.0,
                    'taxes_id': None
                })

            discount_line = self.env['sale.order.line'].search([
                ('order_id', '=', sale_order.id),
                ('product_id', '=', discount_product.id),
            ], limit=1)

            if discount_line:
                discount_line.write({
                    'price_unit': rec.discount_id.discount,  
                })
            else:
                self.env['sale.order.line'].create({
                    'order_id': sale_order.id,
                    'product_id': discount_product.id,
                    'name': rec.discount_id.name,  
                    'product_uom_qty': 1,
                    'price_unit': rec.discount_id.discount,  
                })

