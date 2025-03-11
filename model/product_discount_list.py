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

class sale_order_line(models.Model):
    _inherit="sale.order.line"

    percent_and_fixed_discount= fields.Float(string="Discount",)
    # percentage_discount_bool= fields.Float(string="Discount")
    price_unit = fields.Float(string="Total With Discount",required=True)
    actual_price = fields.Float(string="Unit Price", readonly=True, compute="_compute_price", store=True)

    on_hand_qty= fields.Float(string="On hand qty", compute="_compute_onhand_field")

    @api.depends('product_id')
    def _compute_onhand_field(self):
        for record in self:
            prod_qty = self.env['stock.quant'].search([('product_id', '=', record.product_id.id)], limit=1)
            record.on_hand_qty = prod_qty.inventory_quantity_auto_apply if prod_qty else 0.0


    @api.onchange('product_id', 'order_id.pricelist_id')
    def _onchange_field(self):
        for rec in self:
            if rec.product_id and rec.order_id.pricelist_id:
                pricelist_item = self.env['product.pricelist.item'].search([
                    ('pricelist_id', '=', rec.order_id.pricelist_id.id),
                    ('product_tmpl_id', '=', rec.product_id.product_tmpl_id.id)
                ], limit=1)
                
                if pricelist_item:
                    if pricelist_item.percent_price:
                        if not rec.percent_and_fixed_discount:
                            rec.percent_and_fixed_discount = pricelist_item.percent_price

                        if not (pricelist_item.min_perce_disc <= rec.percent_and_fixed_discount <= pricelist_item.max_perce_disc):
                            raise UserError(
                                f"Discount must be between {pricelist_item.min_perce_disc} and {pricelist_item.max_perce_disc}."
                            )
                    elif pricelist_item.fixed_discount:
                        if not rec.percent_and_fixed_discount:
                            rec.percent_and_fixed_discount = pricelist_item.fixed_discount

                        if not (pricelist_item.min_fix_disc <= rec.percent_and_fixed_discount <= pricelist_item.max_fix_disc):
                            raise UserError(
                                f"Discount must be between {pricelist_item.min_fix_disc} and {pricelist_item.max_fix_disc}."
                            )

    @api.constrains('percent_and_fixed_discount', 'product_id', 'order_id.pricelist_id')
    def _check_discount_limits(self):
        for rec in self:
            if rec.product_id and rec.order_id.pricelist_id:
                pricelist_item = self.env['product.pricelist.item'].search([
                    ('pricelist_id', '=', rec.order_id.pricelist_id.id),
                    ('product_tmpl_id', '=', rec.product_id.product_tmpl_id.id)
                ], limit=1)
                
                if pricelist_item:
                    if pricelist_item.percent_price:
                        if not (pricelist_item.min_perce_disc <= rec.percent_and_fixed_discount <= pricelist_item.max_perce_disc):
                            raise ValidationError(
                                f"Discount must be between {pricelist_item.min_perce_disc} and {pricelist_item.max_perce_disc} for product {rec.product_id.name}."
                            )
                    elif pricelist_item.fixed_discount:
                        if not (pricelist_item.min_fix_disc <= rec.percent_and_fixed_discount <= pricelist_item.max_fix_disc):
                            raise ValidationError(
                                f"Discount must be between {pricelist_item.min_fix_disc} and {pricelist_item.max_fix_disc} for product {rec.product_id.name}."
                            )


    @api.depends('product_template_id', 'product_id',)
    def _compute_price(self):
        for rec in self:
            rec.actual_price=rec.product_template_id.list_price

    @api.depends('product_template_id', 'product_id', 'percent_and_fixed_discount')
    def _compute_price_unit(self):
        super(sale_order_line, self)._compute_price_unit()
        for rec in self:
            pricelist_item = self.env['product.pricelist.item'].search([
                ('pricelist_id', '=', rec.order_id.pricelist_id.id),
                ('product_tmpl_id', '=', rec.product_id.product_tmpl_id.id)
            ], limit=1)
            single_unit=""
            if pricelist_item.percent_price:
                single_unit = rec.actual_price - ((rec.actual_price * rec.percent_and_fixed_discount) / 100)
                # if rec.product_uom_qty > 1:
                rec.price_unit = rec.product_uom_qty * single_unit
            elif pricelist_item.fixed_discount:
                rec.price_unit = rec.price_unit - (rec.product_uom_qty * rec.percent_and_fixed_discount)
            else:
                rec.price_unit = rec.product_template_id.list_price


