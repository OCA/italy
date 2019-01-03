# -*- coding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2012 Associazione OpenERP Italia
#    (<http://www.openerp-italia.org>). 
#    Copyright (C) 2012 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2012 Domsense srl (<http://www.domsense.com>)
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

from osv import fields,osv

class res_partner_contact(osv.osv):
    _inherit = "res.partner.contact"
    _columns = {
        'fiscalcode': fields.char('Fiscal Code', size=16, help="Italian Fiscal Code"),
        }
res_partner_contact()

#class res_partner_location(osv.osv):
#    _inherit = 'res.partner.location'
#    _columns = {
#        'province': fields.many2one('res.province', string='Province'),
#        }
#        
#    def on_change_city(self, cr, uid, ids, city):
#        return self.pool.get('res.partner.address').on_change_city(cr, uid, ids, city)
#        
#    def create(self, cr, uid, vals, context=None):
#        vals = self.pool.get('res.partner.address')._set_vals_city_data(cr, uid, vals)
#        return super(res_partner_location, self).create(cr, uid, vals, context)
#
#    def write(self, cr, uid, ids, vals, context=None):
#        vals = self.pool.get('res.partner.address')._set_vals_city_data(cr, uid, vals)
#        return super(res_partner_location, self).write(cr, uid, ids, vals, context)
#res_partner_location()

#class res_partner_address(osv.osv):
#    _inherit = 'res.partner.address'
#    #_columns = {
#    #    # fields from location
#    #    'province': fields.related('location_id', 'province', string='Province', type="many2one", relation="res.province", store=True),
#    #    }
#    
#    def onchange_location_id(self,cr, uid, ids, location_id=False, context={}):
#        res = super(res_partner_address, self).onchange_location_id(
#            cr, uid, ids, location_id=location_id, context=context)
#        if location_id:
#            location = self.pool.get('res.partner.location').browse(cr, uid, location_id, context=context)
#            res['value'].update({
#                'province':location.province and location.province.id or False,
#                'region':location.province and location.province.region and location.province.region.id or False,
#                })
#        return res
#
#res_partner_address()
