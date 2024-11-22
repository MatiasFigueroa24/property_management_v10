# -*- coding: utf-8 -*-
###############################################################################
#
#   OpenERP, Open Source Management Solution
#   Copyright (C) 2011-Today Serpent Consulting Services PVT LTD
#    (<http://www.serpentcs.com>)
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF

import calendar
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from odoo.tools import float_compare, float_is_zero


class AccountAssetAppreciationLine(models.Model):
    _name = 'account.asset.appreciation.line'
    _description = 'Asset Appreciation line'

    @api.multi
    @api.depends('move_id')
    def get_move_check(self):
        for line in self:
            line.move_check = bool(line.move_id)

    @api.multi
    @api.depends('move_id.state')
    def get_move_posted_check(self):
        """
        If the move id or move state is posted the move posted_check will be true.
        """
        for line in self:
            line.move_posted_check = True if line.move_id and \
                line.move_id.state == 'posted' else False

    name = fields.Char(
        string='Appreciation Name',
        index=True)
    sequence = fields.Integer(
        string='Sequence')
    asset_id = fields.Many2one(
        comodel_name='account.asset.asset',
        string='Asset',
        ondelete='cascade')
    parent_state = fields.Selection(
        related='asset_id.state',
        string='State of Asset')
    amount = fields.Float(
        string='Current Appreciation',
        digits=0)
    remaining_value = fields.Float(
        string='Next Period Appreciation',
        digits=0)
    appreciated_value = fields.Float(
        string='Cumulative Appreciation')
    appreciation_date = fields.Date(
        string='Appreciation Date',
        index=True)
    move_id = fields.Many2one(
        comodel_name='account.move',
        string='Depreciation Entry')
    move_check = fields.Boolean(
        string='Linked',
        compute='get_move_check',
        track_visibility='always',
        store=True)
    move_posted_check = fields.Boolean(
        string='Posted',
        compute='get_move_posted_check',
        track_visibility='always',
        store=True)

    @api.multi
    def create_move(self, post_move=True):
        account_move = self.env['account.move']
        prec = self.env['decimal.precision'].precision_get('Account')
        for line in self:
            appreciation_date = self.env.context.get(
                'appreciation_date') or line.appreciation_date or fields.Date.context_today(self)
            asset_name = line.asset_id.name + \
                ' (%s/%s)' % (line.sequence,
                              len(line.asset_id.appreciation_line_ids))
            category_id = line.asset_id.category_id
            company_currency = line.asset_id.company_id.currency_id
            current_currency = line.asset_id.currency_id
            amount = current_currency.compute(line.amount, company_currency)
            move_line_1 = {
                'name': asset_name,
                'account_id': category_id.account_asset_id.id,
                'debit': amount if float_compare(amount, 0.0, precision_digits=prec) > 0 else 0.0,
                'credit': 0.0 if float_compare(amount, 0.0, precision_digits=prec) > 0 else -amount,
                'journal_id': category_id.journal_id.id,
                'partner_id': line.asset_id.partner_id.id,
                'analytic_account_id': category_id.account_analytic_id.id if category_id.type == 'sale' else False,
                'currency_id': company_currency != current_currency and current_currency.id or False,
                'amount_currency': company_currency != current_currency and - 1.0 * line.amount or 0.0,
            }

            move_line_2 = {
                'name': asset_name,
                'account_id': category_id.account_asset_id.id,
                'debit': 0.0 if float_compare(amount, 0.0, precision_digits=prec) > 0 else -amount,
                'credit': amount if float_compare(amount, 0.0, precision_digits=prec) > 0 else 0.0,
                'journal_id': category_id.journal_id.id,
                'partner_id': line.asset_id.partner_id.id,
                'analytic_account_id': category_id.account_analytic_id.id if category_id.type == 'sale' else False,
                'currency_id': company_currency != current_currency and current_currency.id or False,
                'amount_currency': company_currency != current_currency and - 1.0 * line.amount or 0.0,
            }

            move_vals = {
                'ref': line.asset_id.code,
                'date': appreciation_date or False,
                'journal_id': category_id.journal_id.id,
                'line_ids': [(0, 0, move_line_1), (0, 0, move_line_2)],
            }

            move = account_move.create(move_vals)
            line.write({'move_id': move.id, 'move_check': True})
            account_move |= move


class AccountAssetAsset(models.Model):
    _inherit = 'account.asset.asset'
    _description = 'Asset'

    @api.one
    @api.depends('appr_value', 'appr_salvage_value',
                 'appreciation_line_ids.move_check',
                 'appreciation_line_ids.amount')
    def _amount_residuals(self):
        """
        This method calculate the Total Value  
        """
        total_amount = 0.0
        for line in self.appreciation_line_ids:
            if line.move_check:
                total_amount += line.amount
        self.appr_value_residual = self.appr_salvage_value + \
            self.appr_value + total_amount

    @api.onchange('unit_price', 'gfa_feet')
    def unit_price_calc(self):
        """
        when you change Unit Price and GFA Feet fields value,
        this method will change Total Price and Purchase Value
        accordingly.
        @param self: The object pointer
        """
        res = super(AccountAssetAsset, self).unit_price_calc()
        if self.unit_price and self.gfa_feet:
            self.appr_value = float(self.unit_price * self.gfa_feet)
        if self.unit_price and not self.gfa_feet:
            raise ValidationError(_('Please Insert GFA(Sqft) Please'))
        return res

    @api.multi
    def _get_last_appreciation_date(self):
        """
        @param id: ids of a account.asset.asset objects
        @return: Returns a dictionary of the effective dates of the last
            appreciation entry made for given asset ids. If there isn't any,
            return the purchase date of this asset
        """
        self.env.cr.execute("""
            SELECT a.id as id, COALESCE(MAX(m.date),a.age_of_property) AS age_of_property
            FROM account_asset_asset a
            LEFT JOIN account_asset_appreciation_line rel ON (rel.asset_id = a.id)
            LEFT JOIN account_move m ON (rel.move_id = m.id)
            WHERE a.id IN %s
            GROUP BY a.id, m.date """, (tuple(self.ids),))
        result = dict(self.env.cr.fetchall())
        return result

    def compute_board_amount(self, sequence, residual_amount,
                             amount_to_appr, undone_dotation_number,
                             posted_appreciation_line_ids, total_days,
                             appreciation_date):
        """
        This method calculate bord amount using various calculation method
        like linear and degressive and prorata
        @param id: ids of a account.asset.asset objects
        @param self: The object pointer
        """
        amount = 0
        if sequence == 1:
            amount = residual_amount
        else:
            if self.appr_method == 'linear':
                amount = amount_to_appr / (
                    undone_dotation_number - len(posted_appreciation_line_ids))
                if self.appr_prorata:
                    amount = amount_to_appr / self.appr_method_number
                    if sequence == 1:
                        if self.appr_method_period:
                            date = datetime.strptime(
                                self.age_of_property, '%Y-%m-%d')
                            month_days = calendar.monthrange(
                                date.year, date.month)[1]
                            days = month_days - date.day + 1
                            amount = (
                                amount_to_appr / self.appr_method_number) / month_days * days
                        else:
                            days = (self.company_id.compute_fiscalyear_dates(
                                appreciation_date)['date_to'] - appreciation_date).days + 1
                            amount = (
                                amount_to_appr / self.appr_method_number) / total_days * days
            elif self.appr_method == 'degressive':
                amount = self.appr_value_residual * self.appr_method_progress_factor
                if self.appr_prorata:
                    if sequence == 1:
                        if self.appr_method_period % 12 != 0:
                            date = datetime.strptime(self.date, '%Y-%m-%d')
                            month_days = calendar.monthrange(
                                date.year, date.month)[1]
                            days = month_days - date.day + 1
                            amount = (
                                residual_amount * self.method_progress_factor) / month_days * days
                        else:
                            days = (self.company_id.compute_fiscalyear_dates(
                                appreciation_date)['date_to'] - appreciation_date).days + 1
                            amount = (
                                residual_amount * self.method_progress_factor) / total_days * days
        return amount

    def compute_board_undone_dotation_nb(self, appreciation_date, total_days):
        undone_dotation_number = self.appr_method_number
        if self.appr_method_time == 'end':
            end_date = datetime.strptime(self.appr_method_end, DF).date()
            undone_dotation_number = 0
            while appreciation_date <= end_date:
                appreciation_date = date(
                    appreciation_date.year, appreciation_date.month,
                    appreciation_date.day) + relativedelta(
                        months=+self.appr_method_period)
                undone_dotation_number += 1
        if self.appr_prorata:
            undone_dotation_number += 1
        return undone_dotation_number

    @api.multi
    def compute_appreciation_board(self):
        """
        This method Claculate appreciation bord qas per the selecated method
        value.
        @param id: ids of a account.asset.asset objects
        @param self: The object pointer
        """
        self.ensure_one()

        posted_appreciation_line_ids = self.appreciation_line_ids.filtered(
            lambda x: x.move_check).sorted(key=lambda l: l.appreciation_date)
        unposted_appreciation_line_ids = self.appreciation_line_ids.filtered(
            lambda x: not x.move_check)
        data = [(2, line_id.id, False)
                for line_id in unposted_appreciation_line_ids]
        if self.appr_value_residual != 0.0:
            amount_to_appr = residual_amount = self.appr_value_residual
            if self.appr_prorata:
                if posted_appreciation_line_ids and \
                        posted_appreciation_line_ids[-1].appreciation_date:
                    last_appreciation_date = datetime.strptime(
                        posted_appreciation_line_ids[-1].appreciation_date, DF).date()
                    appreciation_date = last_appreciation_date + \
                        relativedelta(months=+self.app_method_period)
                else:
                    appreciation_date = datetime.strptime(
                        self._get_last_appreciation_date()[self.id], DF).date()
            else:
                if self.appr_method_period >= 12:
                    asset_date = datetime.strptime(
                        self.age_of_property[:4] + '-01-01', DF).date()
                else:
                    asset_date = datetime.strptime(
                        self.age_of_property[:7] + '-01', DF).date()
                if posted_appreciation_line_ids and \
                        posted_appreciation_line_ids[-1].appreciation_date:
                    last_depreciation_date = datetime.strptime(
                        posted_appreciation_line_ids[-1].appreciation_date, DF).date()
                    appreciation_date = last_depreciation_date + \
                        relativedelta(months=+self.appr_method_period)
                else:
                    appreciation_date = asset_date

            day = appreciation_date.day
            month = appreciation_date.month
            year = appreciation_date.year
            total_days = (year % 4) and 365 or 366
#
            undone_dotation_number = self.compute_board_undone_dotation_nb(
                appreciation_date, total_days)

            for x in range(len(
                    posted_appreciation_line_ids), undone_dotation_number):
                sequence = x + 1
                amount = self.compute_board_amount(sequence, residual_amount,
                                                   amount_to_appr,
                                                   undone_dotation_number,
                                                   posted_appreciation_line_ids,
                                                   total_days,
                                                   appreciation_date)
                residual_amount -= amount
                vals = {
                    'appreciation_date': appreciation_date.strftime(DF),
                    'appreciated_value': self.appr_value + (
                        self.appr_salvage_value - residual_amount),
                    'amount': amount,
                    'remaining_value':  abs(residual_amount),
                    'asset_id': self.id,
                    'sequence': sequence,
                    'name': (self.code or '') + '/' + str(sequence),
                }
                data.append((0, False, vals))
                appreciation_date = date(
                    year, month, day) + relativedelta(
                        months=+self.appr_method_period)
                day = appreciation_date.day
                month = appreciation_date.month
                year = appreciation_date.year
        self.write({'appreciation_line_ids': data})
        return True

    appreciation_line_ids = fields.One2many(
        'account.asset.appreciation.line', 'asset_id',
        string='Appreciation Lines',
        states={'draft': [('readonly', False)], 'open': [('readonly', False)]})
    appr_value = fields.Float(
        string='Gross Value',
        digits=0,
        states={'draft': [('readonly', False)]})
    appr_salvage_value = fields.Float(
        string='Increase Value',
        digits=0,
        states={'draft': [('readonly', False)]})
    appr_value_residual = fields.Float(
        compute='_amount_residuals',
        method=True,
        digits=0,
        string='Total Value')
    appr_method = fields.Selection(
        [('linear', 'Linear'), ('degressive', 'Degressive')],
        string='Computation Method',
        states={'draft': [('readonly', False)]},
        default='linear')
    appr_method_progress_factor = fields.Float(
        string='Degressive Factor',
        default=0.3,
        states={'draft': [('readonly', False)]})
    appr_method_time = fields.Selection(
        [('number', 'Number of Appreciations'), ('end', 'Ending Date')],
        string='Time Method',
        default='number',
        states={'draft': [('readonly', False)]})
    appr_prorata = fields.Boolean(
        string='Prorata Temporis',
        states={'draft': [('readonly', False)]})
    appr_method_number = fields.Integer(
        string='Number of Appreciations',
        states={'draft': [('readonly', False)]},
        default=5)
    appr_method_period = fields.Integer(
        string='Number of Months in a Period',
        default=12,
        states={'draft': [('readonly', False)]})
    appr_method_end = fields.Date(
        string='Ending Date',
        states={'draft': [('readonly', False)]})

    @api.model
    def create(self, vals):
        """
        When asset or property craeted that time call the
        compute_appreciation_board and calculate amount.
        @param id: ids of a account.asset.asset objects
        @param self: The object pointer
        """
        assets = super(AccountAssetAsset, self).create(vals)
        assets.compute_appreciation_board()
        return assets
