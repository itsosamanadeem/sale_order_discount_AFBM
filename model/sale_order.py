from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = "sale.order"

    iscategory = fields.Boolean(string="Is Category", default=True)

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

        if order.type_id and order.type_id.name == 'POS type':
            order.action_confirm()

            # Ensure all related deliveries are validated
            for picking in order.picking_ids.filtered(lambda p: p.state not in ['done', 'cancel']):
                try:
                    picking.button_validate()
                except Exception as e:
                    _logger.error("Error while validating picking: %s", e)

        return order
