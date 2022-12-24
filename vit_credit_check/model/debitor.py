#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class debitor(models.Model):

    _name = "res.partner"
    _description = "res.partner"
    _inherit = "res.partner"

    credit_status = fields.Char( string="Credit status",  help="", )


    credit_history_ids = fields.One2many(comodel_name="vit.credit_history",  inverse_name="partner_id",  string="Credit history",  help="", )
    owner_id = fields.Many2one(comodel_name="res.partner",  string="Owner",  help="", )
