# -*- coding: utf-8 -*-
##############################################################################
#    
# Copyright (C) 2012 Agile Business Group sagl (<http://www.agilebg.com>)
# Copyright (C) 2012 Domsense srl (<http://www.domsense.com>)
# Copyright (C) 2012 Associazione Odoo Italia
# (<http://www.odoo-italia.org>).
# Copyright (C) 2016 Andrea Cometa (Apulia Software)
# Email: a.cometa@apuliasoftware.it
# Copyright (C) 2016 KTec S.r.l.
# (<http://www.ktec.it>).
#
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
#
##############################################################################


from odoo import models, fields, tools, api, _
from odoo.addons import decimal_precision as dp


class RibaDistinta(models.Model):

    _name = 'riba.distinta'
    _description = 'Distinta Ricevute Bancarie'

    name = fields.Char(
        'Reference', size=128, required=True, readonly=True,
        states={'draft': [('readonly', False)]},
        default="_get_sequence"
    )
    config = fields.Many2one(
        'riba.configurazione', 'Configuration', index=True, required=True,
        readonly=True, states={'draft': [('readonly', False)]},
        help="Riba configuration to be used")
    state = fields.Selection([
            ('draft', 'Draft'),
            ('accepted', 'Accepted'),
            ('accredited', 'Accredited'),
            ('paid', 'Paid'),
            ('unsolved', 'Unsolved'),
            ('cancel', 'Canceled')], "State", index=True, readonly=True)
    line_ids = fields.One2many(
        'riba.distinta.line', 'distinta_id', "Riba deadlines", readonly=True,
        states={'draft': [('readonly', False)]}),
    user_id = fields.Many2one(
        'res.users', "User", required=True, readonly=True,
        states={'draft': [('readonly', False)]},
        default=lambda self: self.env.user)
    date_created = fields.Date(
        "Creation date", readonly=True, default=fields.Date.context_today)
    date_accepted = fields.Date("Acceptance date", readonly=True)
    date_accreditation = fields.Date("Accreditation date", readonly=True)
    date_paid = fields.Date("Paid date", readonly=True)
    date_unsolved = fields.Date("Unsolved date", readonly=True)
    company_id = fields.Many2one(
        'res.company', "Company", required=True, readonly=True,
        states={'draft': [('readonly', False)]},
        default=lambda self: self.env.company_id.id,
    )
    acceptance_move_ids = fields.Many2many(
        compute='_get_acceptance_move_ids', relation='account.move',
        string="Acceptance Entries")
    accreditation_move_id = fields.Many2one(
        'account.move', "Accreditation Entry", readonly=True)
    payment_ids = fields.Many2many(
        compute='_get_payment_ids', relation='account.move.line',
        string='Payments')
    unsolved_move_ids = fields.Many2many(
        compute='_get_unsolved_move_ids', relation='account.move',
        method=True, string="Unsolved Entries")
    type = fields.Selection(
        related='config.tipo', size=32, string='Type', readonly=True)
    registration_date = fields.Date(
        "Registration Date",
        states={'draft': [('readonly', False)],
                'cancel': [('readonly', False)], },
        index=True, readonly=True, required=True,
        default=fields.Date.context_today,
        help="Keep empty to use the current date")

    @api.depends('line_ids')
    def _get_acceptance_move_ids(self):
        for distinta in self:
            move_ids = []
            for line in distinta.line_ids:
                if line.acceptance_move_id and line.acceptance_move_id.id not in move_ids:
                    move_ids.append(line.acceptance_move_id.id)
            distinta.acceptance_move_ids = move_ids

    @api.depends('line_ids')
    def _get_unsolved_move_ids(self):
        for distinta in self:
            move_ids = []
            for line in distinta.line_ids:
                if line.unsolved_move_id and line.unsolved_move_id.id not in move_ids:
                    move_ids.append(line.unsolved_move_id.id)
            distinta.unsolved_move_ids = move_ids

    @api.depends('line_ids')
    def _get_payment_ids(self):
        for distinta in self:
            move_line_ids = []
            for line in distinta.line_ids:
                for payment in line.payment_ids:
                    if payment.id not in move_line_ids:
                        move_line_ids.append(payment.id)
            distinta.payment_ids = move_line_ids

    def _get_sequence(self):
        return self.env['ir.sequence'].get('riba.distinta')

    #ToDO: incompleto da sistemare
    @api.multi
    def unlink(self):
        for distinta in self:
            if distinta.state not in ('draft',  'cancel'):
                raise orm.except_orm(_('Error'),
                                     _('Distinta %s is in state %s. '
                                       'You can only delete documents '
                                       'in state draft or canceled')
                                     % (distinta.name, distinta.state))
        super(RibaDistinta,self).unlink()
        return True

    def confirm(self):
        for distinta in self:
            distinta.line_ids.confirm()

    #ToDO: rivedere, forse è il caso di usare default
    @api.multi
    def riba_new(self):
        for distinta in self:
            distinta.state = 'draft'

    @api.multi
    def riba_cancel(self):
        for distinta in self:
            # TODO remove ervery other move
            for line in distinta.line_ids:
                if line.acceptance_move_id:
                    line.acceptance_move_id.unlink()
                if line.unsolved_move_id:
                    line.unsolved_move_id.unlink()
            if distinta.accreditation_move_id:
                distinta.accreditation_move_id.unlink()
            distinta.state = 'cancel'

    @api.multi
    def riba_accepted(self):
        for distinta in self:
            distinta.state = 'acccepted'
            distinta.date_accepted = fields.Date.context_today()

    @api.multi
    def riba_accredited(self):
        for distinta in self:
            for line in distinta
                line.state = 'accredited'
            distinta.state = 'accredited'
            distinta.date_accreditation = fields.Date.context_today()

    @api.multi
    def riba_paid(self):
        for distinta in self:
            distinta.state = 'paid'
            distinta.date_paid = fields.Date.context_today()

    @api.multi
    def riba_unsolved(self, cr, uid, ids, context=None):
        for distinta in self:
            distinta.state = 'state'
            distinta.date_unsolved = fields.Date.context_today()

    @api.multi
    def test_accepted(self):
        for distinta in self:
            for line in distinta.line_ids:
                if line.state != 'confirmed':
                    return False
        return True

    @api.multi
    def test_unsolved(self):
        for distinta in self:
            for line in distinta.line_ids:
                if line.state != 'unsolved':
                    return False
        return True

    @api.multi
    def test_paid(self):
        for distinta in self:
            for line in distinta.line_ids:
                if line.state != 'paid':
                    return False
        return True

    #ToDO: da migrare ... che fa il metodo trg_delete????
    def action_cancel_draft(self, cr, uid, ids, *args):
        self.write(cr, uid, ids, {'state': 'draft'})
        for distinta_id in ids:
            self.trg_delete(uid, 'riba.distinta', distinta_id, cr)
            self.trg_create(uid, 'riba.distinta', distinta_id, cr)
        return True


class RibaDistintaLine(models.Model):

    # TODO estendere la account_due_list per visualizzare e filtrare in base alle riba ?
    _name = 'riba.distinta.line'
    _description = "Riba details"

    sequence = fields.Integer("Number")
    move_line_ids = fields.One2many(
        'riba.distinta.move.line', 'riba_line_id', "Credit move lines")
    acceptance_move_id = fields.Many2one(
        'account.move', "Acceptance Entry", readonly=True)
    unsolved_move_id = fields.Many2one(
        'account.move', "Unsolved Entry", readonly=True)
    acceptance_account_id = fields.Many2one(
        'account.account', "Acceptance Account")
    amount = fields.Float(
        compute='_get_line_values', method=True, string="Amount", multi="line")
    bank_id = fields.Many2one('res.partner.bank', "Debitor Bank")
    iban = fields.Char(  # FIX ?
        related='bank_id.acc_number', string='IBAN', store=False, readonly=True)
    distinta_id = fields.Many2one(
        'riba.distinta', "Distinta", required=True, ondelete='cascade')
    partner_id = fields.Many2one(
        'res.partner', "Customer", readonly=True)
    invoice_date = fields.Char(
        compute='_get_line_values', string="Invoice Date", size=256,
        method=True, multi="line")
    invoice_number = fields.Char(
        compute='_get_line_values', string="Invoice Number", size=256,
        method=True, multi="line")
    due_date = fields.Date("Due date", readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('accredited', 'Accredited'),
        ('paid', 'Paid'),
        ('unsolved', 'Unsolved'),
        ], "State", index=True, readonly=True)
    reconciled = fields.Boolean(
        compute='_reconciled', string='Paid/Reconciled',
        store={
            'riba.distinta.line': (lambda self, cr, uid, ids, c={}: ids, ['acceptance_move_id'], 50),
            'account.move.line': (_get_riba_line_from_move_line, None, 50),
            'account.move.reconcile': (_get_line_from_reconcile, None, 50),
        }, help="It indicates that the line has been paid and the journal entry of the line has been reconciled with one or several journal entries of payment."),
    payment_ids = fields.Many2many(
        compute='_compute_lines', relation='account.move.line',
        string='Payments')
    type = fields.Selection(
        related='distinta_id.type', size=32, string='Type', readonly=True)
    
    def _get_line_values(self):
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            res[line.id] = {}
            res[line.id]['amount'] = 0.0
            res[line.id]['invoice_date'] = ''
            res[line.id]['invoice_number'] = ''
            for move_line in line.move_line_ids:
                res[line.id]['amount'] += move_line.amount
                if not res[line.id]['invoice_date']:
                    res[line.id]['invoice_date'] = str(move_line.move_line_id.invoice.date_invoice)
                else:
                    res[line.id]['invoice_date'] += ', '+str(move_line.move_line_id.invoice.date_invoice)
                if not res[line.id]['invoice_number']:
                    res[line.id]['invoice_number'] = str(move_line.move_line_id.invoice.internal_number)
                else:
                    res[line.id]['invoice_number'] += ', '+str(move_line.move_line_id.invoice.internal_number)
        return res

    def _reconciled(self, cr, uid, ids, name, args, context=None):
        res = {}
        for id in ids:
            res[id] = self.test_paid(cr, uid, [id])
            if res[id]:
                self.write(cr, uid, id, {'state': 'paid'}, context=context)
                self.trg_validate(
                    uid, 'riba.distinta',
                    self.browse(cr, uid, id).distinta_id.id, 'paid', cr)
        return res

    def move_line_id_payment_gets(self, cr, uid, ids, *args):
        res = {}
        if not ids: return res
        cr.execute('SELECT distinta_line.id, l.id '\
                   'FROM account_move_line l '\
                   'LEFT JOIN riba_distinta_line distinta_line ON (distinta_line.acceptance_move_id=l.move_id) '\
                   'WHERE distinta_line.id IN %s '\
                   'AND l.account_id=distinta_line.acceptance_account_id',
                   (tuple(ids),))
        for r in cr.fetchall():
            res.setdefault(r[0], [])
            res[r[0]].append( r[1] )
        return res

    # return the ids of the move lines which has the same account than the statement
    # whose id is in ids
    def move_line_id_payment_get(self, cr, uid, ids, *args):
        if not ids: return []
        result = self.move_line_id_payment_gets(cr, uid, ids, *args)
        return result.get(ids[0], [])

    def test_paid(self, cr, uid, ids, *args):
        res = self.move_line_id_payment_get(cr, uid, ids)
        if not res:
            return False
        ok = True
        for id in res:
            cr.execute('select reconcile_id from account_move_line where id=%s', (id,))
            ok = ok and  bool(cr.fetchone()[0])
        return ok

    def _get_riba_line_from_move_line(self, cr, uid, ids, context=None):
        move = {}
        for line in self.pool.get('account.move.line').browse(cr, uid, ids, context=context):
            if line.reconcile_partial_id:
                for line2 in line.reconcile_partial_id.line_partial_ids:
                    move[line2.move_id.id] = True
            if line.reconcile_id:
                for line2 in line.reconcile_id.line_id:
                    move[line2.move_id.id] = True
        line_ids = []
        if move:
            line_ids = self.pool.get('riba.distinta.line').search(
                cr, uid, [('acceptance_move_id','in',move.keys())], context=context)
        return line_ids

    def _get_line_from_reconcile(self, cr, uid, ids, context=None):
        move = {}
        for r in self.pool.get('account.move.reconcile').browse(cr, uid, ids, context=context):
            for line in r.line_partial_ids:
                move[line.move_id.id] = True
            for line in r.line_id:
                move[line.move_id.id] = True
        line_ids = []
        if move:
            line_ids = self.pool.get('riba.distinta.line').search(
                cr, uid, [('acceptance_move_id','in',move.keys())], context=context)
        return line_ids

    def _compute_lines(self, cr, uid, ids, name, args, context=None):
        result = {}
        for riba_line in self.browse(cr, uid, ids, context=context):
            src = []
            lines = []
            if riba_line.acceptance_move_id:
                for m in riba_line.acceptance_move_id.line_id:
                    temp_lines = []
                    if m.reconcile_id and m.credit == 0.0:
                        temp_lines = map(lambda x: x.id, m.reconcile_id.line_id)
                    elif m.reconcile_partial_id and m.credit == 0.0:
                        temp_lines = map(lambda x: x.id, m.reconcile_partial_id.line_partial_ids)
                    lines += [x for x in temp_lines if x not in lines]
                    src.append(m.id)

            lines = filter(lambda x: x not in src, lines)
            result[riba_line.id] = lines
        return result

    #ToDO: da verificare
    @api.multi
    def confirm(self):
        move_pool = self.env['account.move']
        move_line_pool = self.env['account.move.line']
        for line in self.browse(cr, uid, ids, context=context):
            journal = line.distinta_id.config.acceptance_journal_id
            total_credit = 0.0
            move_id= move_pool.create(cr, uid, {
                'ref': 'Ri.Ba. %s - line %s' % (line.distinta_id.name, line.sequence),
                'journal_id': journal.id,
                'date': line.distinta_id.registration_date,
                }, context=context)
            to_be_reconciled = []
            for riba_move_line in line.move_line_ids:
                total_credit += riba_move_line.amount
                move_line_id = move_line_pool.create(cr, uid, {
                    'name': riba_move_line.move_line_id.invoice.number,
                    'partner_id': line.partner_id.id,
                    'account_id': riba_move_line.move_line_id.account_id.id,
                    'credit': riba_move_line.amount,
                    'debit': 0.0,
                    'move_id': move_id,
                    }, context=context)
                to_be_reconciled.append([move_line_id, riba_move_line.move_line_id.id])
            move_line_pool.create(cr, uid, {
                'name': 'Ri.Ba. %s - line %s' % (line.distinta_id.name, line.sequence),
                'account_id': (
                    line.acceptance_account_id.id or
                    line.distinta_id.config.acceptance_account_id.id
                    # in questo modo se la riga non ha conto accettazione
                    # viene prelevato il conto in configurazione riba
                    ),
                'partner_id': line.partner_id.id,
                'date_maturity': line.due_date,
                'credit': 0.0,
                'debit': total_credit,
                'move_id': move_id,
                }, context=context)
            move_pool.post(cr, uid, [move_id], context=context)
            for reconcile_ids in to_be_reconciled:
                move_line_pool.reconcile_partial(cr, uid, reconcile_ids, context=context)
            line.write({
                'acceptance_move_id': move_id,
                'state': 'confirmed',
                })
            self.trg_validate(
                uid, 'riba.distinta', line.distinta_id.id, 'accepted', cr)
        return True


class RibaDistintaMoveLine(models.Model):

    _name = 'riba.distinta.move.line'
    _description = 'Riba details'
    _rec_name = 'amount'

    amount= fields.Float("Amount", digits_compute=dp.get_precision('Account'))
    move_line_id = fields.Many2one('account.move.line', "Credit move line")
    riba_line_id = fields.Many2one(
        'riba.distinta.line', "Distinta line", ondelete='cascade')

