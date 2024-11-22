# -*- coding: utf-8 -*-
###############################################################################
#
# 	OpenERP, Open Source Management Solution
# 	Copyright (C) 2011-Today Serpent Consulting Services PVT LTD
# 	(<http://www.serpentcs.com>)
#
# 	This program is free software: you can redistribute it and/or modify
# 	it under the terms of the GNU Affero General Public License as
# 	published by the Free Software Foundation, either version 3 of the
# 	License, or (at your option) any later version.
#
# 	This program is distributed in the hope that it will be useful,
# 	but WITHOUT ANY WARRANTY; without even the implied warranty of
# 	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# 	GNU Affero General Public License for more details.
#
# 	You should have received a copy of the GNU Affero General Public License
# 	along with this program.  If not, see <http://www.gnu.org/licenses/>.
###############################################################################
from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import Warning, UserError
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class AccountAnalyticAccount(models.Model):
    _inherit = "account.analytic.account"

    is_tenancy_rent = fields.Boolean(
        string='Is Tenancy Rent?')
    prop_ids = fields.Many2one(
        comodel_name='account.asset.asset',
        string='Property',
        help="Name of property")
    property_owner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Owner',
        help="Owner of property.")

    @api.onchange('property_id')
    def onchange_property_id(self):
        """
        This Method is used to set property related fields value,
        on change of property.
        ------------------------------------------------------------
        @param self: The object pointer
        """
        if self.property_id:
            self.rent = self.property_id.ground_rent or False
            self.rent_type_id = self.property_id.rent_type_id and \
                self.property_id.rent_type_id.id or False

    @api.onchange('prop_ids')
    def onchange_prop_ids(self):
        """
        This Method is used to set property related fields value,
        on change of property.
        ----------------------------------------------------------
        @param self: The object pointer
        """
        if self._context.get('is_tenancy_rent'):
            if self.prop_ids:
                self.rent = self.prop_ids.ground_rent or False
                self.property_owner_id = self.prop_ids.property_manager.id or \
                    False
                self.rent_type_id = self.prop_ids.rent_type_id and \
                    self.prop_ids.rent_type_id.id or False

    @api.model
    def create(self, vals):
        """
        This Method is used to overrides orm create method,
        to change state and tenant of related property.
        ---------------------------------------------------
        @param self: The object pointer
        @param vals: dictionary of fields value.
        """
        res = super(AccountAnalyticAccount, self).create(vals)
        if self._context.get('is_tenancy_rent'):
            res.ref = self.env['ir.sequence'].get(
                'tenancy.rent')
            if res.is_tenancy_rent:
                res.write({'is_property': False})
            if 'prop_ids' in vals:
                prop_brw = self.env['account.asset.asset'].browse(
                    vals['prop_ids'])
                prop_brw.write({'state': 'book'})
        return res

    @api.multi
    def write(self, vals):
        """
        This Method is used to overrides orm write method,
        to change state and tenant of related property.
        ------------------------------------------------
        @param self: The object pointer
        @param vals: dictionary of fields value.
        """
        rec = super(AccountAnalyticAccount, self).write(vals)
        if self.is_tenancy_rent:
            for tenancy_rec in self:
                if vals.get('state'):
                    if vals['state'] == 'open':
                        tenancy_rec.prop_ids.write({'state': 'normal'})
                    if vals['state'] == 'close':
                        tenancy_rec.prop_ids.write(
                            {'state': 'draft'})
        return rec

    @api.multi
    def button_starts(self):
        """
        This button method is used to Change Tenancy state to Open.
        ------------------------------------------------------------
        @param self: The object pointer
        """
        if self._context.get('is_tenancy_rent'):
            for current_rec in self:
                if current_rec.prop_ids.property_manager and \
                        current_rec.prop_ids.property_manager.id:
                    releted_user = current_rec.prop_ids.property_manager.id
                    new_ids = self.env['res.users'].search(
                        [('partner_id', '=', releted_user)])
                    if releted_user and new_ids and new_ids.ids:
                        new_ids.write(
                            {'tenant_ids': [(4, current_rec.tenant_id.id)]})
            self.write({'state': 'open', 'rent_entry_chck': False})

    @api.multi
    def unlink(self):
        """
        Overrides orm unlink method,
        ------------------------------
        @param self: The object pointer
        @return: True/False.
        """
        if self._context.get('is_tenancy_rent'):
            rent_ids = []
            for tenancy_rec in self:
                analytic_ids = self.env['account.analytic.line'].search(
                    [('account_id', '=', tenancy_rec.id)])
                if analytic_ids and analytic_ids.ids:
                    analytic_ids.unlink()
                rent_ids = self.env['tenancy.rent.schedule'].search(
                    [('tenancy_id', '=', tenancy_rec.id)])
                post_rent = [x.id for x in rent_ids if x.move_check is True]
                if post_rent:
                    raise Warning(
                        _('You cannot delete Tenancy record, if any related \
                        Rent Schedule entries are in posted.'))
                else:
                    rent_ids.unlink()
                if tenancy_rec.prop_ids.property_manager and \
                        tenancy_rec.prop_ids.property_manager.id:
                    releted_user = tenancy_rec.prop_ids.property_manager.id
                    new_ids = self.env['res.users'].search(
                        [('partner_id', '=', releted_user)])
                tenancy_rec.prop_ids.write(
                    {'state': 'draft'})
        return super(AccountAnalyticAccount, self).unlink()

    @api.multi
    def button_return(self):
        """
        This method create supplier invoice for returning deposite
        amount.
        -----------------------------------------------------------
        @param self: The object pointer
        """
        if self._context.get('is_tenancy_rent'):
            data = self
            inv_line_values = {
                'name': 'Deposit Return' or "",
                'origin': 'account.analytic.account' or "",
                'quantity': 1,
                'account_id': data.prop_ids.income_acc_id.id or False,
                'price_unit': data.deposit or 0.00,
                'account_analytic_id': data.id or False,
            }
            inv_values = {
                'origin': 'Deposit Return For ' + data.name or "",
                'type': 'in_invoice',
                'property_id': data.prop_ids.id,
                'partner_id': data.property_owner_id.id or False,
                'account_id': data.property_owner_id.property_account_payable_id.id or False,
                'invoice_line_ids': [(0, 0, inv_line_values)],
                'date_invoice': datetime.now().strftime(
                    DEFAULT_SERVER_DATE_FORMAT) or False,
                'new_tenancy_id': data.id,
            }
            acc_id = self.env['account.invoice'].create(inv_values)
            self.write({'invc_id': acc_id.id})
            wiz_form_id = self.env['ir.model.data'].get_object_reference(
                'account', 'invoice_supplier_form')[1]
            return {
                'view_type': 'form',
                'view_id': wiz_form_id,
                'view_mode': 'form',
                'res_model': 'account.invoice',
                'res_id': self.invc_id.id,
                'type': 'ir.actions.act_window',
                'target': 'current',
                'context': self._context,
            }
        return super(AccountAnalyticAccount, self).button_return()

    @api.multi
    def button_receive(self):
        """
        This button method is used to open the related
        account payment form view.
        ------------------------------------------------
        @param self: The object pointer
        @return: Dictionary of values.
        """
        if self._context.get('is_tenancy_rent'):
            if not self._ids:
                return []
            for tenancy_rec in self:
                if tenancy_rec.acc_pay_dep_rec_id and \
                        tenancy_rec.acc_pay_dep_rec_id.id:
                    acc_pay_form_id = self.env['ir.model.data'].get_object_reference(
                        'account', 'view_account_payment_form')[1]
                    return {
                        'view_type': 'form',
                        'view_id': acc_pay_form_id,
                        'view_mode': 'form',
                        'res_model': 'account.payment',
                        'res_id': self.acc_pay_dep_rec_id.id,
                        'type': 'ir.actions.act_window',
                        'target': 'current',
                        'context': self._context,
                    }
                if tenancy_rec.deposit == 0.00:
                    raise Warning(_('Please Enter Deposit amount.'))
                if not tenancy_rec.prop_ids.income_acc_id.id:
                    raise Warning(
                        _('Please Configure Income Account from Property.'))
                ir_id = self.env['ir.model.data']._get_id(
                    'account', 'view_account_payment_form')
                ir_rec = self.env['ir.model.data'].browse(ir_id)
                return {
                    'view_mode': 'form',
                    'view_id': [ir_rec.res_id],
                    'view_type': 'form',
                    'res_model': 'account.payment',
                    'type': 'ir.actions.act_window',
                    'nodestroy': True,
                    'target': 'current',
                    'domain': '[]',
                    'context': {
                        'default_partner_id': tenancy_rec.property_owner_id.id,
                        'default_partner_type': 'customer',
                        'default_journal_id': 6,
                        'default_payment_type': 'inbound',
                        'default_communication': 'Deposit Received',
                        'default_tenancy_id': tenancy_rec.id,
                        'default_amount': tenancy_rec.deposit,
                        'default_property_id': tenancy_rec.prop_ids.id,
                        'close_after_process': True,
                    }
                }
        return super(AccountAnalyticAccount, self).button_receive()

    @api.multi
    def create_rent_schedule(self):
        """
        This button method is used to create rent schedule Lines.
        ------------------------------------------------------------
        @param self: The object pointer
        """
        rent_obj = self.env['tenancy.rent.schedule']
        for tenancy_rec in self:
            if tenancy_rec.rent_type_id.renttype == 'Weekly':
                d1 = datetime.strptime(
                    tenancy_rec.date_start, DEFAULT_SERVER_DATE_FORMAT)
                d2 = datetime.strptime(
                    tenancy_rec.date, DEFAULT_SERVER_DATE_FORMAT)
                interval = int(tenancy_rec.rent_type_id.name)
                if d2 < d1:
                    raise Warning(
                        _('End date must be greater than start date.'))
                wek_diff = (d2 - d1)
                wek_tot1 = (wek_diff.days) / (interval * 7)
                wek_tot = (wek_diff.days) % (interval * 7)
                if wek_diff.days == 0:
                    wek_tot = 1
                if wek_tot1 > 0:
                    for wek_rec in range(wek_tot1):
                        rent_obj1 = rent_obj.create({
                            'start_date': d1.strftime
                            (DEFAULT_SERVER_DATE_FORMAT),
                            'amount': tenancy_rec.rent * interval
                            or 0.0,
                            'property_id': tenancy_rec.property_id
                            and tenancy_rec.property_id.id or False,
                            'tenancy_id': tenancy_rec.id,
                            'currency_id': tenancy_rec.currency_id.id or False,
                            'rel_tenant_id': tenancy_rec.tenant_id.id
                        })
                        if self._context.get('is_tenancy_rent') or self.is_tenancy_rent:
                            rent_obj1.update({'property_id': tenancy_rec.prop_ids
                                              and tenancy_rec.prop_ids.id or False})
                        d1 = d1 + relativedelta(days=(7 * interval))
                if wek_tot > 0:
                    one_day_rent = 0.0
                    if tenancy_rec.rent:
                        one_day_rent = (tenancy_rec.rent) / (7 * interval)
                    rent_obj2 = rent_obj.create({
                        'start_date': d1.strftime
                        (DEFAULT_SERVER_DATE_FORMAT),
                        'amount': (one_day_rent * (wek_tot)) or 0.0,
                        'property_id': tenancy_rec.property_id
                        and tenancy_rec.property_id.id or False,
                        'tenancy_id': tenancy_rec.id,
                        'currency_id': tenancy_rec.currency_id.id
                        or False,
                        'rel_tenant_id': tenancy_rec.tenant_id.id
                    })
                    if self._context.get('is_tenancy_rent') or self.is_tenancy_rent:
                        rent_obj2.update({'property_id': tenancy_rec.prop_ids
                                          and tenancy_rec.prop_ids.id or False})
            elif tenancy_rec.rent_type_id.renttype != 'Weekly':
                if tenancy_rec.rent_type_id.renttype == 'Monthly':
                    interval = int(tenancy_rec.rent_type_id.name)
                if tenancy_rec.rent_type_id.renttype == 'Yearly':
                    interval = int(tenancy_rec.rent_type_id.name) * 12
                d1 = datetime.strptime(
                    tenancy_rec.date_start, DEFAULT_SERVER_DATE_FORMAT)
                d2 = datetime.strptime(
                    tenancy_rec.date, DEFAULT_SERVER_DATE_FORMAT)
                diff = abs((d1.year - d2.year) * 12 + (d1.month - d2.month))
                tot_rec = diff / interval
                tot_rec2 = diff % interval
                if abs(d1.month - d2.month) >= 0 and d1.day < d2.day:
                    tot_rec2 += 1
                if diff == 0:
                    tot_rec2 = 1
                if tot_rec > 0:
                    for rec in range(tot_rec):
                        rent_obj3 = rent_obj.create({
                            'start_date': d1.strftime
                            (DEFAULT_SERVER_DATE_FORMAT),
                            'amount': tenancy_rec.rent * interval
                            or 0.0,
                            'property_id': tenancy_rec.prop_ids
                            and tenancy_rec.prop_ids.id or False,
                            'tenancy_id': tenancy_rec.id,
                            'currency_id': tenancy_rec.currency_id.id or False,
                            'rel_tenant_id': tenancy_rec.tenant_id.id
                        })
                        if self._context.get('is_tenancy_rent') or self.is_tenancy_rent:
                            rent_obj3.update({'property_id': tenancy_rec.prop_ids
                                              and tenancy_rec.prop_ids.id or False})
                        d1 = d1 + relativedelta(months=interval)
                if tot_rec2 > 0:
                    rent_obj4 = rent_obj.create({
                        'start_date': d1.strftime(DEFAULT_SERVER_DATE_FORMAT),
                        'amount': tenancy_rec.rent * tot_rec2 or 0.0,
                        'property_id': tenancy_rec.prop_ids and
                        tenancy_rec.prop_ids.id or False,
                        'tenancy_id': tenancy_rec.id,
                        'currency_id': tenancy_rec.currency_id.id or False,
                        'rel_tenant_id': tenancy_rec.tenant_id.id
                    })
                    if self._context.get('is_tenancy_rent') or \
                            self.is_tenancy_rent:
                        rent_obj4.update(
                            {'property_id': tenancy_rec.prop_ids and
                                tenancy_rec.prop_ids.id or False})
        return self.write({'rent_entry_chck': True})


class TenancyRentSchedule(models.Model):
    _inherit = "tenancy.rent.schedule"
    _rec_name = "tenancy_id"

    @api.multi
    def create_invoice(self):
        """
        Create invoice for Rent Schedule.
        ------------------------------------
        @param self: The object pointer
        """
        if self.tenancy_id.is_tenancy_rent:
            inv_lines_values = {
                'origin': 'tenancy.rent.schedule',
                'name': 'Tenancy(Rent) Cost for' + self.tenancy_id.name,
                'quantity': 1,
                'price_unit': self.amount or 0.00,
                'account_id': self.tenancy_id.prop_ids.expense_account_id.id or False,
                'account_analytic_id': self.tenancy_id.id or False,
            }
            if self._context.get('penanlty') == 0:
                self.calculate_penalty()
                if self.tenancy_id.penalty < 00:
                    raise Warning(_('The Penalty% must be strictly positive.'))
                if self.tenancy_id.penalty_day < 00:
                    raise Warning(_('The Penalty Count After Days must be \
                    strictly positive.'))
                amt = self.amount + self.penalty_amount
                inv_lines_values.update({'price_unit': amt or 0.00})
            if self.tenancy_id.multi_prop:
                for data in self.tenancy_id.prop_id:
                    for account in data.property_ids.expense_account_id:
                        account_id = account.id
                inv_lines_values.update({'account_id': account_id})
            if self.tenancy_id.main_cost >= 0.00:
                if self.tenancy_id.main_cost:
                    inv_line_main = {
                        'origin': 'tenancy.rent.schedule',
                        'name': 'Maintenance cost',
                        'price_unit': self.tenancy_id.main_cost or 0.00,
                        'quantity': 1,
                        'account_id': self.tenancy_id.prop_ids.expense_account_id.id or False,
                        'account_analytic_id': self.tenancy_id.id or False,
                    }
                    if self.tenancy_id.multi_prop:
                        for data in self.tenancy_id.prop_id:
                            for account in data.property_ids.expense_account_id:
                                inv_line_main.update(
                                    {'account_id': account.id})
            invo_values = {
                'partner_id': self.tenancy_id.property_owner_id.id or False,
                'type': 'in_invoice',
                'invoice_line_ids': [(0, 0, inv_lines_values)],
                'property_id': self.tenancy_id.prop_ids.id or False,
                'date_invoice': datetime.now().strftime(
                    DEFAULT_SERVER_DATE_FORMAT) or False,
                'account_id': self.tenancy_id.property_owner_id.property_account_payable_id.id,
            }
            if self._context.get('recuring') == 0:
                if self.tenancy_id.main_cost:
                    invo_values.update(
                        {'invoice_line_ids': [(0, 0, inv_lines_values),
                                              (0, 0, inv_line_main)]})
                else:
                    invo_values.update(
                        {'invoice_line_ids': [(0, 0, inv_lines_values)]})

            acc_id = self.env['account.invoice'].create(invo_values)
            self.write({'invc_id': acc_id.id, 'inv': True})
            wiz_form_id = self.env['ir.model.data'].get_object_reference(
                'account', 'invoice_supplier_form')[1]
            return {
                'view_type': 'form',
                'view_id': wiz_form_id,
                'view_mode': 'form',
                'res_model': 'account.invoice',
                'res_id': self.invc_id.id,
                'type': 'ir.actions.act_window',
                'target': 'current',
                'context': self._context,
            }
        return super(TenancyRentSchedule, self).create_invoice()

    @api.multi
    def open_invoice(self):
        """
        Description:
            This method is used to open invoce which is created.
        
        Decorators:
            api.multi
        """
        if self.tenancy_id.is_tenancy_rent is True:
            context = dict(self._context or {})
            wiz_form_id = self.env['ir.model.data'].get_object_reference(
                'account', 'invoice_supplier_form')[1]
            return {
                'view_type': 'form',
                'view_id': wiz_form_id,
                'view_mode': 'form',
                'res_model': 'account.invoice',
                'res_id': self.invc_id.id,
                'type': 'ir.actions.act_window',
                'target': 'current',
                'context': context,
            }
        return super(TenancyRentSchedule, self).open_invoice()
