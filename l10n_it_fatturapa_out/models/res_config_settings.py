# Copyright 2014 Davide Corio
# Copyright 2015-2016 Lorenzo Battistini - Agile Business Group
# Copyright 2020 Matteo Mircoli Openforce srls

from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    phone_electronic_invoice = fields.Char(
        related='company_id.phone_electronic_invoice',
        readonly=False,
    )


