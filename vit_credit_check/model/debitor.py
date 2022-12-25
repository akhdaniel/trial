#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class debitor(models.Model):

    _name = "vit.debitor"
    _description = "vit.debitor"
    name = fields.Char( required=True, string="Name",  help="", )
    email = fields.Char( string="Email",  help="", )
    address = fields.Text( string="Address",  help="", )
    mobile = fields.Char( string="Mobile",  help="", )
    phone = fields.Char( string="Phone",  help="", )
    city = fields.Char( string="City",  help="", )
    country = fields.Char( string="Country",  help="", )
    credit_score = fields.Char( string="Credit score",  help="", )


    credit_history_ids = fields.One2many(comodel_name="vit.credit_history",  inverse_name="debitor_id",  string="Credit history",  help="", )
    owner_id = fields.Many2one(comodel_name="res.company",  string="Owner",  help="", )
