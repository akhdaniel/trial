#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class owner(models.Model):

    _name = "res.company"
    _description = "res.company"
    _inherit = "res.company"



