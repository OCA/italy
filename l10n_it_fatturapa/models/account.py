# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 Davide Corio <davide.corio@lsweb.it>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from . import attachment
from openerp.osv import fields, orm


class fatturapa_document_type(orm.Model):
    _name = "fatturapa.document_type"
    _description = 'FatturaPA Document Type'

    _columns = {
        'name': fields.char('Description', size=128),
        'code': fields.char('Code', size=4),
    }


class fatturapa_payment_term(orm.Model):
    _name = "fatturapa.payment_term"
    _description = 'FatturaPA Payment Term'

    _columns = {
        'name': fields.char('Description', size=128),
        'code': fields.char('Code', size=4),
    }


class fatturapa_payment_method(orm.Model):
    _name = "fatturapa.payment_method"
    _description = 'FatturaPA Payment Method'

    _columns = {
        'name': fields.char('Description', size=128),
        'code': fields.char('Code', size=4),
    }


class fatturapa_fiscal_position(orm.Model):
    _name = "fatturapa.fiscal_position"
    _description = 'FatturaPA Fiscal Position'

    _columns = {
        'name': fields.char('Description', size=128),
        'code': fields.char('Code', size=4),
    }


class fatturapa_format(orm.Model):
    _name = "fatturapa.format"
    _description = 'FatturaPA Format'

    _columns = {
        'name': fields.char('Description', size=128),
        'code': fields.char('Code', size=5),
    }


class account_payment_term(orm.Model):
    _inherit = 'account.payment.term'

    _columns = {
        'fatturapa_pt_id': fields.many2one(
            'fatturapa.payment_term', string="FatturaPA Payment Term"),
        'fatturapa_pm_id': fields.many2one(
            'fatturapa.payment_method', string="FatturaPA Payment Method"),
    }


class account_invoice(orm.Model):
    _inherit = "account.invoice"

    _columns = {
        'fatturapa_po_enable': fields.boolean('FatturaPA Purchase Order'),
        'fatturapa_po': fields.char(
            'FatturaPA Purchase Order Number', size=64),
        'fatturapa_po_line_no': fields.integer('FatturaPA PO Line No'),
        'fatturapa_po_cup': fields.char('FatturaPA PO CUP', size=64),
        'fatturapa_po_cig': fields.char('FatturaPA PO CIG', size=64),
        'fatturapa_contract_enable': fields.boolean('FatturaPA Contract'),
        'fatturapa_contract': fields.char(
            'FatturaPA Contract Number', size=64),
        'fatturapa_contract_line_no': fields.char(
            'FatturaPA Contract Line No', size=12),
        'fatturapa_contract_date': fields.date('FatturaPA Contract Date'),
        'fatturapa_contract_numitem': fields.char(
            'FatturaPA Contract NumItem', size=64),
        'fatturapa_contract_cup': fields.char(
            'FatturaPA Contract CUP', size=64),
        'fatturapa_contract_cig': fields.char(
            'FatturaPA Contract CIG', size=64),
        'fatturapa_agreement_enable': fields.boolean('FatturaPA Agreement'),
        'fatturapa_agreement': fields.char(
            'FatturaPA Agreement Number', size=64),
        'fatturapa_agreement_line_no': fields.char(
            'FatturaPA Agreement Line No', size=12),
        'fatturapa_agreement_date': fields.date('FatturaPA Agreement Date'),
        'fatturapa_agreement_numitem': fields.char(
            'FatturaPA Agreement NumItem', size=64),
        'fatturapa_agreement_cup': fields.char(
            'FatturaPA Agreement CUP', size=64),
        'fatturapa_agreement_cig': fields.char(
            'FatturaPA Agreement CIG', size=64),
        'fatturapa_reception_enable': fields.boolean('FatturaPA Reception'),
        'fatturapa_reception': fields.char(
            'FatturaPA Reception Number', size=64),
        'fatturapa_reception_line_no': fields.char(
            'FatturaPA Reception Line No', size=12),
        'fatturapa_reception_date': fields.date('FatturaPA Reception Date'),
        'fatturapa_reception_numitem': fields.char(
            'FatturaPA Reception NumItem', size=64),
        'fatturapa_reception_cup': fields.char(
            'FatturaPA Reception CUP', size=64),
        'fatturapa_reception_cig': fields.char(
            'FatturaPA Reception CIG', size=64),
        'fatturapa_attachment_id': fields.many2one(
            'fatturapa.attachment', 'FatturaPA Export File'),
        'fatturapa_attachment_state': fields.related(
            'fatturapa_attachment_id', 'state', type='selection', store=True,
            selection=attachment.AVAILABLE_STATES, readonly=True, select=True,
            string='FatturaPA Export State'),
    }
