# © 2016 Andrea Cometa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class DistintaReportQweb(models.AbstractModel):

    _name = 'report.l10n_it_ricevute_bancarie.distinta_qweb'
    _description = "Report Ri.Ba. list"

    @api.multi
    def get_report_values(self, docids, data=None):
        return {
            'doc_ids': docids,
            'doc_model': 'riba.distinta',
            'docs': self.env['riba.distinta'].browse(docids),
            'data': data,
        }
