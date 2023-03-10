from odoo import api, fields, models, _
import time
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class ConfimWizard(models.TransientModel):
    _name = 'vit.confirm_wizard'

    quantity = fields.Integer('Records to generate', default=1000)

    # @api.multi
    def confirm_button(self):
        self.ensure_one()
        emp = self.env['vit.temp_partner']
        emp.dummy_create_partners(self.quantity)
        return {'type':'ir.actions.act_window_close'}