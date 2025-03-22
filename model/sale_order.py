from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit="sale.order"

    iscategory= fields.Boolean(string="Is Category", default=True)

    def action_open_selection_discount_wizard(self):
        self.ensure_one()
        return {
            'name': _("Miscellaneous Charges"),
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order.selection.discount',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_sale_order_id': self.id},
        }
    
    @api.model
    def create(self, vals):
        order = super(SaleOrder, self).create(vals)

        # Check if type_id is POS
        if order.type_id and order.type_id.name == 'POS type':
            # Confirm the sale order
            order.action_confirm()

            # Find the related delivery order (stock picking)
            picking = order.picking_ids.filtered(lambda p: p.state not in ('done', 'cancel'))

            if picking:
                # Confirm and assign stock
                picking.action_confirm()
                picking.action_assign()

                # Set quantity done and validate
                # for move in picking.move_ids_without_package:
                #     for move_line in move.move_line_ids:
                #         move_line.qty_done = move_line.product_uom_id 

                picking.button_validate()  
                picking.send_sms()

        return order