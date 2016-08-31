# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Associazione Odoo Italia
#    (<http://www.odoo-italia.org>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api, _
from openerp.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

try:
    import codicefiscale
except ImportError:
    _logger.warning(
        'codicefiscale library not found. '
        'If you plan to use it, please install the codicefiscale library '
        'from https://pypi.python.org/pypi/codicefiscale')


class ResPartner(models.Model):
    _inherit = 'res.partner'

    fiscalcode = fields.Char(
        string='Fiscal Code', size=16, help="Italian Fiscal Code")
    individual = fields.Boolean(
        string='Individual', default=False,
        help="If checked the C.F. is referred to a Individual Person")

    @api.multi
    @api.constrains('fiscalcode')
    def _check_fiscalcode(self):

        for partner in self:
            if partner.fiscalcode:
                if partner.is_company and len(partner.fiscalcode) != 11 and \
                        not partner.individual and not partner.fiscalcode.isdigit():
                    raise ValidationError(
                        _("Company fiscal code must be 11 digts lenght.")
                    )
                elif len(partner.fiscalcode) != 16 and \
                        not codicefiscale.isvalid(partner.fiscalcode):
                    raise ValidationError(
                        _("The fiscal code doesn't seem to be correct.")
                    )
