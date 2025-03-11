# from odoo import models, fields, api
# from odoo.exceptions import UserError
# import logging
# _logger = logging.getLogger(__name__)

# class SaleOrderLine(models.Model):

#     _inherit="sale.order.line"

#     fixed_discount_tree= fields.Float(string="Fixed Discount")
#     # fixed_discount_tree_bool= fields.Float(string="Fixed Discount")
#     percentage_discount= fields.Float(string="Percentage Discount")
#     discount= fields.Float(string="Discount")
#     # price_unit = fields.Float(string="Total With Discount",required=True)
#     actual_price = fields.Float(string="Unit Price", readonly=True, compute="_compute_price", store=True)

#     @api.onchange('product_id', 'order_id.pricelist_id','percentage_discount','fixed_discount_tree')
#     def _onchange_actuall_discount(self):
#         pricelist_item = self.env['product.pricelist.item'].search([
#             ('pricelist_id', '=', self.order_id.pricelist_id.id),
#             ('product_tmpl_id', '=', self.product_id.product_tmpl_id.id)
#         ], limit=1)

#         if pricelist_item.percent_price != 0:
#             dis= self.discount
#             if self.discount <= pricelist_item.percent_price:
#                 # discount= pricelist_item.fixed_discount
#                 if dis and (dis <= pricelist_item.percent_price):
#                     self.discount = dis
#                 else:
#                     self.discount = pricelist_item.percent_price
#             elif self.discount > pricelist_item.percent_price:
#                 raise UserError(f"You cannot increase the set fixed discount to {self.discount}!")
#         elif pricelist_item:
#             dis= self.discount
#             if self.discount <= pricelist_item.fixed_discount:
#                 # discount= pricelist_item.fixed_discount
#                 if dis and (dis <= pricelist_item.fixed_discount):
#                     self.discount = dis
#                 else:
#                     self.discount = pricelist_item.fixed_discount
#             elif self.discount > pricelist_item.fixed_discount:
#                 raise UserError(f"You cannot increase the set fixed discount to {self.discount}!")
#         else:
#             self.discount = 0.0
#             self.discount = 0.0


#     @api.depends('product_template_id', 'product_id',)
#     def _compute_price(self):
#         for rec in self:
#             rec.actual_price=rec.product_id.list_price

#     # @api.depends('actual_price', 'discount')
#     # def _compute_price_unit(self):
#     #     super(SaleOrderLine, self)._compute_price_unit()
        
#     #     for rec in self:
#     #         rec.price_unit = rec.actual_price  
#     #         pricelist_item = self.env['product.pricelist.item'].search([
#     #             ('pricelist_id', '=', self.order_id.pricelist_id.id),
#     #             ('product_tmpl_id', '=', self.product_id.product_tmpl_id.id)
#     #         ], limit=1)
#     #         if pricelist_item.percent_price:
#     #             rec.price_unit -= (rec.actual_price * rec.discount) / 100
#     #         if pricelist_item.fixed_discount:
#     #             rec.price_unit -= rec.discount
            
#     @api.depends('price_unit', 'product_uom_qty')
#     def _compute_amount(self):
#         super(SaleOrderLine, self)._compute_amount()
#         for rec in self:
#             rec.update({
#                 "price_total" : rec.price_unit * rec.product_uom_qty
#             })
        