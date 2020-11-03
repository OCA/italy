# Copyright 2014 Davide Corio
# Copyright 2015-2016 Lorenzo Battistini - Agile Business Group
# Copyright 2020 Matteo Mircoli Openforce srls

from odoo import fields, models, api


class ResCompany(models.Model):
    _inherit = "res.company"

    phone_electronic_invoice = fields.Char(
      string="Phone for Electronic Invoice"
    )
