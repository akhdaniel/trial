#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class credit_history(models.Model):

    _name = "vit.credit_history"
    _description = "vit.credit_history"
    name = fields.Char( required=True, string="Name",  help="", )
    date_from = fields.Date( string="Date from",  help="", )
    date_to = fields.Date( string="Date to",  help="", )
    amount = fields.Float( string="Amount",  help="", )
    provider = fields.Char( string="Provider",  help="", )


    debitor_id = fields.Many2one(comodel_name="vit.debitor",  string="Debitor",  help="", )
