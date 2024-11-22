# -*- coding: utf-8 -*-
###############################################################################
#
#   OpenERP, Open Source Management Solution
#   Copyright (C) 2011-Today Serpent Consulting Services PVT LTD
#   (<http://www.serpentcs.com>)
#
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
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
###############################################################################
import re
import threading

from datetime import datetime
from odoo.exceptions import Warning, except_orm, ValidationError
from odoo import models, fields, api, sql_db, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class TenantPartner(models.Model):
    _name = "tenant.partner"
    _inherits = {'res.partner': 'parent_id'}

    doc_name = fields.Char(
        string='Filename')
    id_attachment = fields.Binary(
        string='Identity Proof')
    tenancy_ids = fields.One2many(
        comodel_name='account.analytic.account',
        inverse_name='tenant_id',
        string='Tenancy Details',
        help='Tenancy Details')
    parent_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner',
        required=True,
        index=True,
        ondelete='cascade')
    tenant_ids = fields.Many2many(
        comodel_name='tenant.partner',
        relation='agent_tenant_rel',
        column1='agent_id',
        column2='tenant_id',
        string='Tenant Details',
        domain=[('customer', '=', True), ('agent', '=', False)])
    mobile = fields.Char(
        string='Mobile',
        size=15)
    maintenance_ids = fields.One2many(
        comodel_name='property.maintenance',
        inverse_name='tenant_id',
        string='Maintenance Details')

    @api.constrains('mobile')
    def _check_value_tp(self):
        """
        Check the mobile number in special formate if you enter wrong
        mobile formate then raise ValidationError
        """
        for val in self:
            if val.mobile:
                if re.match("^\+|[1-9]{1}[0-9]{3,14}$", val.mobile) != None:
                    pass
                else:
                    raise ValidationError('Please Enter Valid Mobile Number')

    @api.constrains('email')
    def _check_values_tp(self):
        """
        Check the email address in special formate if you enter wrong
        mobile formate then raise ValidationError
        """
        for val in self:
            if val.email:
                if re.match("^[a-zA-Z0-9._+-]+@[a-zA-Z0-9]+\.[a-zA-Z0-9.]*\.*[a-zA-Z]{2,4}$", val.email) != None:
                    pass
                else:
                    raise ValidationError('Please Enter Valid Email Id')

    @api.model
    def create(self, vals):
        """
        This Method is used to overrides orm create method.
        @param self: The object pointer
        @param vals: dictionary of fields value.
        """
        dataobj = self.env['ir.model.data']
        property_user = False
        res = super(TenantPartner, self).create(vals)
        password = self.env['res.company'].browse(
            vals.get('company_id', False)).default_password
        if not password:
            password = ''
        create_user = self.env['res.users'].create({
            'login': vals.get('email'),
            'name': vals.get('name'),
            'password': password,
            'tenant_id': res.id,
            'partner_id': res.parent_id.id,
        })
        if res.customer:
            property_user = dataobj.get_object_reference(
                'property_management', 'group_property_user')
        if res.agent:
            property_user = dataobj.get_object_reference(
                'property_management', 'group_property_agent')
        if property_user:
            grop_id = self.env['res.groups'].browse(property_user[1])
            grop_id.write({'users': [(4, create_user.id)]})
        return res

    @api.model
    def default_get(self, fields):
        """
        This method is used to gets default values for tenant.
        @param self: The object pointer
        @param fields: Names of fields.
        @return: Dictionary of values.
        """
        context = dict(self._context or {})
        res = super(TenantPartner, self).default_get(fields)
        if context.get('tenant', False):
            res.update({'tenant': context['tenant']})
        res.update({'customer': True})
        return res

    @api.multi
    def unlink(self):
        """
        Overrides orm unlink method.
        @param self: The object pointer
        @return: True/False.
        """
        for tenant_rec in self:
            if tenant_rec.parent_id and tenant_rec.parent_id.id:
                releted_user = tenant_rec.parent_id.id
                new_user_rec = self.env['res.users'].search(
                    [('partner_id', '=', releted_user)])
                if releted_user and new_user_rec and new_user_rec.ids:
                    new_user_rec.unlink()
        return super(TenantPartner, self).unlink()


class PropertyType(models.Model):
    _name = "property.type"

    name = fields.Char(
        string='Name',
        size=50,
        required=True)


class RentType(models.Model):
    _name = "rent.type"
    _order = 'sequence_in_view'

    @api.multi
    @api.depends('name', 'renttype')
    def name_get(self):
        """
        Added name_get for purpose of displaying company name with renttype
        """
        res = []
        for rec in self:
            rec_str = ''
            if rec.name:
                rec_str += rec.name
            if rec.renttype:
                rec_str += ' ' + rec.renttype
            res.append((rec.id, rec_str))
        return res

    @api.model
    def name_search(self, name='', args=[], operator='ilike', limit=100):
        """
         Added name_search for purpose to search by name and renttype
        """
        args += ['|', ('name', operator, name), ('renttype', operator, name)]
        cuur_ids = self.search(args, limit=limit)
        return cuur_ids.name_get()

    name = fields.Selection(
        [('1', '1'), ('2', '2'), ('3', '3'),
         ('4', '4'), ('5', '5'), ('6', '6'),
         ('7', '7'), ('8', '8'), ('9', '9'),
         ('10', '10'), ('11', '11'), ('12', '12')])

    renttype = fields.Selection(
        [('Monthly', 'Monthly'),
         ('Yearly', 'Yearly'),
         ('Weekly', 'Weekly')],
        string='Rent Type')
    sequence_in_view = fields.Integer(
        string='Sequence')


class RoomType(models.Model):
    _name = "room.type"

    name = fields.Char(
        string='Name',
        size=50,
        required=True)


class Utility(models.Model):
    _name = "utility"

    name = fields.Char(
        string='Name',
        size=50,
        required=True)


class PlaceType(models.Model):
    _name = 'place.type'

    name = fields.Char(
        string='Place Type',
        size=50,
        required=True)


class MaintenanceType(models.Model):
    _name = 'maintenance.type'

    name = fields.Char(
        string='Maintenance Type',
        size=50,
        required=True)


class PropertyPhase(models.Model):
    _name = "property.phase"

    end_date = fields.Date(
        string='End Date')
    start_date = fields.Date(
        string='Beginning Date')
    commercial_tax = fields.Float(
        string='Commercial Tax (in %)')
    occupancy_rate = fields.Float(
        string='Occupancy Rate (in %)')
    lease_price = fields.Float(
        string='Sales/lease Price Per Month')
    phase_id = fields.Many2one(
        comodel_name='account.asset.asset',
        string='Property')
    operational_budget = fields.Float(
        string='Operational Budget (in %)')
    company_income = fields.Float(
        string='Company Income Tax CIT (in %)')


class PropertyPhoto(models.Model):
    _name = "property.photo"

    photos = fields.Binary(
        string='Photos')
    doc_name = fields.Char(
        string='Filename')
    photos_description = fields.Char(
        string='Description')
    photo_id = fields.Many2one(
        comodel_name='account.asset.asset',
        string='Property')


class PropertyRoom(models.Model):
    _name = "property.room"

    note = fields.Text(
        string='Notes')
    width = fields.Float(
        string='Width')
    height = fields.Float(
        string='Height')
    length = fields.Float(
        string='Length')
    image = fields.Binary(
        string='Picture')
    name = fields.Char(
        string='Name',
        size=60)
    attach = fields.Boolean(
        string='Attach Bathroom')
    type_id = fields.Many2one(
        comodel_name='room.type',
        string='Room Type')
    assets_ids = fields.One2many(
        comodel_name='room.assets',
        inverse_name='room_id',
        string='Assets')
    property_id = fields.Many2one(
        comodel_name='account.asset.asset',
        string='Property')


class NearbyProperty(models.Model):
    _name = 'nearby.property'

    distance = fields.Float(
        string='Distance (Km)')
    name = fields.Char(
        string='Name',
        size=100)
    type = fields.Many2one(
        comodel_name='place.type',
        string='Type')
    property_id = fields.Many2one(
        comodel_name='account.asset.asset',
        string='Property')


class PropertyMaintenace(models.Model):
    _name = "property.maintenance"
    _inherit = ['ir.needaction_mixin', 'mail.thread']

    date = fields.Date(
        string='Date',
        default=fields.Date.context_today)
    cost = fields.Float(
        string='Cost')
    type = fields.Many2one(
        comodel_name='maintenance.type',
        string='Type')
    assign_to = fields.Many2one(
        comodel_name='res.partner',
        string='Assign To')
    invc_id = fields.Many2one(
        comodel_name='account.invoice',
        string='Invoice')
    renters_fault = fields.Boolean(
        string='Renters Fault',
        default=False,
        copy=True)
    invc_check = fields.Boolean(
        string='Already Created',
        default=False)
    mail_check = fields.Boolean(
        string='Mail Send',
        default=False)
    property_id = fields.Many2one(
        comodel_name='account.asset.asset',
        string='Property')
    account_code = fields.Many2one(
        comodel_name='account.account',
        string='Account Code')
    notes = fields.Text(
        string='Description',
        size=100)
    name = fields.Selection(
        [('Renew', 'Renew'),
         ('Repair', 'Repair'),
         ('Replace', 'Replace')],
        string='Action',
        default='Repair')
    state = fields.Selection(
        [('draft', 'Draft'),
         ('progress', 'In Progress'),
         ('incomplete', 'Incomplete'),
         ('done', 'Done')],
        string='State',
        default='draft')
    tenant_id = fields.Many2one(
        comodel_name='tenant.partner',
        string='Tenant')

    @api.model
    def _needaction_domain_get(self):
        return [('state', '=', 'draft')]

    @api.multi
    def send_maint_mail(self):
        """
        This Method is used to send an email to assigned person.
        @param self: The object pointer
        """
        try:
            new_cr = sql_db.db_connect(self.env.cr.dbname).cursor()
            uid, context = self.env.uid, self.env.context
            with api.Environment.manage():
                self.env = api.Environment(new_cr, uid, context)
                ir_model_data = self.env['ir.model.data']
                try:
                    if self._context.get('cancel'):
                        template_id = ir_model_data.get_object_reference(
                            'property_management', 'mail_template_property_maintainance_close')[1]
                    if self._context.get('invoice'):
                        template_id = ir_model_data.get_object_reference(
                            'property_management', 'email_template_edi_invoice_id')[1]
                    else:
                        template_id = ir_model_data.get_object_reference(
                            'property_management', 'mail_template_property_maintainance')[1]
                except ValueError:
                    template_id = False
                for maint_rec in self:
                    if not maint_rec.property_id.current_tenant_id.email:
                        raise except_orm(
                            ("Cannot send email: Assigned user has no \
                                email address."), maint_rec.property_id.current_tenant_id.name)
                    self.env['mail.template'].browse(template_id).send_mail(
                        maint_rec.id, force_send=True)
        finally:
            self.env.cr.close()

    @api.multi
    def reopen_maintenance(self):
        """
        This method is use to when maintenance is cancel and we
        needed to reopen maintenance and change state to draft. 
        @param self: The object pointer
        """
        self.write({'state': 'draft'})

    @api.multi
    def start_maint(self):
        """
        This Method is used to change maintenance state to progress.
        @param self: The object pointer
        """
        self.write({'state': 'progress'})
        thrd_cal = threading.Thread(target=self.send_maint_mail)
        thrd_cal.start()

    @api.multi
    def cancel_maint(self):
        """
        This Method is used to change maintenance state to incomplete.
        @param self: The object pointer
        """
        self.write({'state': 'incomplete'})
        thrd_cal = threading.Thread(target=self.send_maint_mail)
        thrd_cal.start()

    @api.onchange('renters_fault')
    def onchange_renters_fault(self):
        """
        If renters fault is true then it assigne the current tennant
        to related property in field and if it false remove tenant
        @param self: The object pointer
        """
        for data in self:
            if data.property_id:
                tncy_ids = self.env['account.analytic.account'].search(
                    [('property_id', '=', data.property_id.id), (
                        'state', '!=', 'close')])
                if tncy_ids:
                    for t in tncy_ids:
                        if data.renters_fault:
                            data.tenant_id = t.tenant_id[0].id
                        else:
                            data.tenant_id = 0
                else:
                     data.tenant_id = False
            else:
                data.tenant_id = False

    @api.onchange('assign_to')
    def onchanchange_assign(self):
        """
        In account code assigne account payable of assigne worker.
        """
        for data in self:
            data.account_code = data.assign_to.property_account_payable_id

    @api.multi
    def create_invoice(self):
        """
        This Method is used to create invoice from maintenance record.
        @param self: The object pointer
        """
        for data in self:
            if not data.account_code:
                raise Warning(_("Please Select Account Code"))
            if not data.property_id.id:
                raise Warning(_("Please Select Property"))
            tncy_ids = self.env['account.analytic.account'].search(
                [('property_id', '=', data.property_id.id),
                 ('state', '!=', 'close')])
            if len(tncy_ids.ids) == 0:
                raise Warning(_("No current tenancy for this property"))
            else:
                for tenancy_data in tncy_ids:
                    inv_line_values = {
                        'name': 'Maintenance For ' + data.type.name or "",
                        'origin': 'property.maintenance',
                        'quantity': 1,
                        'account_id': data.property_id.income_acc_id.id or
                        False,
                        'price_unit': data.cost or 0.00,
                    }

                    inv_values = {
                        'origin': 'Maintenance For ' + data.type.name or "",
                        'type': 'out_invoice',
                        'property_id': data.property_id.id,
                        'partner_id': tenancy_data.tenant_id.parent_id.id or
                        False,
                        'account_id': data.account_code.id or False,
                        'invoice_line_ids': [(0, 0, inv_line_values)],
                        'amount_total': data.cost or 0.0,
                        'date_invoice': datetime.now().strftime(
                            DEFAULT_SERVER_DATE_FORMAT) or False,
                        'number': tenancy_data.name or '',
                    }
                if data.renters_fault:
                    inv_values.update(
                        {'partner_id': tenancy_data.tenant_id.parent_id.id or
                         False})
                else:
                    inv_values.update({
                        'partner_id': tenancy_data.property_id.property_manager.id or False})
                acc_id = self.env['account.invoice'].create(inv_values)
                data.write(
                    {'renters_fault': False,
                     'invc_check': True,
                     'invc_id': acc_id.id,
                     'state': 'done'
                     })
        thrd_cal = threading.Thread(target=self.send_maint_mail)
        thrd_cal.start()
        return True

    @api.multi
    def open_invoice(self):
        """
        This Method is used to Open invoice from maintenance record.
        @param self: The object pointer
        """
        context = dict(self._context or {})
        wiz_form_id = self.env['ir.model.data'].get_object_reference(
            'account', 'invoice_form')[1]
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


class CostCost(models.Model):
    _name = "cost.cost"
    _order = 'date'

    @api.one
    @api.depends('move_id')
    def _get_move_check(self):
        self.move_check = bool(self.move_id)

    date = fields.Date(
        string='Date')
    amount = fields.Float(
        string='Amount')
    name = fields.Char(
        string='Description',
        size=100)
    payment_details = fields.Char(
        string='Payment Details',
        size=100)
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency')
    move_id = fields.Many2one(
        comodel_name='account.move',
        string='Purchase Entry')
    purchase_property_id = fields.Many2one(
        comodel_name='account.asset.asset',
        string='Property')
    remaining_amount = fields.Float(
        string='Remaining Amount',
        help='Shows remaining amount in currency')
    move_check = fields.Boolean(
        compute='_get_move_check',
        method=True,
        string='Posted',
        store=True)
    rmn_amnt_per = fields.Float(
        string='Remaining Amount In %',
        help='Shows remaining amount in Percentage')
    invc_id = fields.Many2one(
        comodel_name='account.invoice',
        string='Invoice')

    @api.multi
    def create_invoice(self):
        """
        This button Method is used to create account invoice.
        @param self: The object pointer
        """
        if not self.purchase_property_id.partner_id:
            raise Warning(_('Please Select Partner'))
        if not self.purchase_property_id.expense_account_id:
            raise Warning(_('Please Select Expense Account'))
        account_jrnl_obj = self.env['account.journal'].search(
            [('type', '=', 'purchase')])

        inv_line_values = {
            'origin': 'Cost.Cost',
            'name': 'Purchase Cost For'+''+self.purchase_property_id.name,
            'price_unit': self.amount or 0.00,
            'quantity': 1,
            'account_id': self.purchase_property_id.expense_account_id.id,
        }

        inv_values = {
            'payment_term_id': self.purchase_property_id.payment_term.id or
            False,
            'partner_id': self.purchase_property_id.partner_id.id or False,
            'type': 'in_invoice',
            'property_id': self.purchase_property_id.id or False,
            'invoice_line_ids': [(0, 0, inv_line_values)],
            'date_invoice': datetime.now().strftime(
                DEFAULT_SERVER_DATE_FORMAT) or False,
            'journal_id': account_jrnl_obj.id or False,
        }
        acc_id = self.env['account.invoice'].create(inv_values)
        self.write({'invc_id': acc_id.id, 'move_check': True})
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

    @api.multi
    def open_invoice(self):
        """
        This Method is used to Open invoice
        @param self: The object pointer
        """
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


class RoomAssets(models.Model):
    _name = "room.assets"

    date = fields.Date(
        string='Date')
    name = fields.Char(
        string='Description',
        size=60)
    type = fields.Selection(
        [('fixed', 'Fixed Assets'),
         ('movable', 'Movable Assets'),
         ('other', 'Other Assets')],
        string='Type')
    qty = fields.Float(
        string='Quantity')
    room_id = fields.Many2one(
        comodel_name='property.room',
        string='Property')


class PropertyInsurance(models.Model):
    _name = "property.insurance"

    premium = fields.Float(
        string='Premium')
    end_date = fields.Date(
        string='End Date')
    doc_name = fields.Char(
        string='Filename')
    contract = fields.Binary(
        string='Contract')
    start_date = fields.Date(
        string='Start Date')
    name = fields.Char(
        string='Description',
        size=60)
    policy_no = fields.Char(
        string='Policy Number',
        size=60)
    contact = fields.Many2one(
        comodel_name='res.company',
        string='Insurance Comapny')
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Related Company')
    property_insurance_id = fields.Many2one(
        comodel_name='account.asset.asset',
        string='Property')
    payment_mode_type = fields.Selection(
        [('monthly', 'Monthly'),
         ('semi_annually', 'Semi Annually'),
         ('yearly', 'Annually')],
        string='Payment Term',
        size=40)


class TenancyRentSchedule(models.Model):
    _name = "tenancy.rent.schedule"
    _rec_name = "tenancy_id"
    _order = 'start_date'

    @api.depends('invc_id.state')
    def _get_move_check(self):
        """
        This method check if invoice state is paid true the move check field.
        @param self: The object pointer
        """
        for data in self:
            data.move_check = bool(data.move_id)
            if data.invc_id:
                if data.invc_id.state == 'paid':
                    data.move_check = True

    @api.depends('invc_id', 'invc_id.state')
    def invoice_paid_true(self):
        """
        If  the invoice state in paid state then paid field will be true.
        @param self: The object pointer
        """
        for data in self:
            if data.invc_id:
                if data.invc_id.state == 'paid':
                    data.paid = True

    note = fields.Text(
        string='Notes',
        help='Additional Notes.')
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        required=True)
    amount = fields.Monetary(
        string='Amount',
        default=0.0,
        currency_field='currency_id',
        help="Rent Amount.")
    start_date = fields.Date(
        string='Date',
        help='Start Date.')
    end_date = fields.Date(
        string='End Date',
        help='End Date.')
    cheque_detail = fields.Char(
        string='Cheque Detail',
        size=30)
    move_check = fields.Boolean(
        compute='_get_move_check',
        method=True,
        string='Posted',
        store=True)
    rel_tenant_id = fields.Many2one(
        comodel_name='tenant.partner',
        string="Tenant")
    move_id = fields.Many2one(
        comodel_name='account.move',
        string='Depreciation Entry')
    property_id = fields.Many2one(
        comodel_name='account.asset.asset',
        string='Property',
        help='Property Name.')
    tenancy_id = fields.Many2one(
        comodel_name='account.analytic.account',
        string='Tenancy',
        help='Tenancy Name.')
    paid = fields.Boolean(
        compute="invoice_paid_true",
        store=True,
        method=True,
        string='Paid',
        help="True if this rent is paid by tenant")
    invc_id = fields.Many2one(
        comodel_name='account.invoice',
        string='Invoice')
    inv = fields.Boolean(
        string='Invoice')
    pen_amt = fields.Float(
        string='Pending Amount',
        help='Pending Ammount.',
        store=True)

    @api.multi
    def create_invoice(self):
        """
        Create invoice for Rent Schedule.
        @param self: The object pointer
        """
        inv_line_values = {
            'origin': 'tenancy.rent.schedule',
            'name': 'Tenancy(Rent) Cost',
            'price_unit': self.amount or 0.00,
            'quantity': 1,
            'account_id': self.tenancy_id.property_id.income_acc_id.id or False,
            'account_analytic_id': self.tenancy_id.id or False,
        }
        if self.tenancy_id.multi_prop:
            for data in self.tenancy_id.prop_id:
                for account in data.property_ids.income_acc_id:
                    inv_line_values.update({'account_id': account.id})
#         if self.tenancy_id.penalty_a is True:
        if self._context.get('penanlty') == 0:
            self.calculate_penalty()
            if self.tenancy_id.penalty < 00:
                raise Warning(_('The Penalty% must be strictly positive.'))
            if self.tenancy_id.penalty_day < 00:
                raise Warning(_('The Penalty Count After Days must be \
                strictly positive.'))
            amt = self.amount + self.penalty_amount
            inv_line_values.update({'price_unit': amt or 0.00})
        if self.tenancy_id.multi_prop:
            for data in self.tenancy_id.prop_id:
                for account in data.property_ids.income_acc_id:
                    inv_line_values.update({'account_id': account.id})
#         if self._context.get('recuring') == 0:
        if self.tenancy_id.main_cost >= 0.00:
            inv_line_main = {
                'origin': 'tenancy.rent.schedule',
                'name': 'Maintenance cost',
                'price_unit': self.tenancy_id.main_cost or 0.00,
                'quantity': 1,
                'account_id': self.tenancy_id.property_id.income_acc_id.id
                or False,
                'account_analytic_id': self.tenancy_id.id or False,
            }
            if self.tenancy_id.rent_type_id.renttype == 'Monthly':
                m = self.tenancy_id.main_cost * \
                    float(self.tenancy_id.rent_type_id.name)
                inv_line_main.update({'price_unit': m})
            if self.tenancy_id.rent_type_id.renttype == 'Yearly':
                y = self.tenancy_id.main_cost * \
                    float(self.tenancy_id.rent_type_id.name) * 12
                inv_line_main.update({'price_unit': y})
            if self.tenancy_id.multi_prop:
                for data in self.tenancy_id.prop_id:
                    for account in data.property_ids.income_acc_id:
                        inv_line_main.update({'account_id': account.id})
        inv_values = {
            'partner_id': self.tenancy_id.tenant_id.parent_id.id or False,
            'type': 'out_invoice',
            'property_id': self.tenancy_id.property_id.id or False,
            'date_invoice': datetime.now().strftime(
                DEFAULT_SERVER_DATE_FORMAT) or False,
            'invoice_line_ids': [(0, 0, inv_line_values)],
        }
        if self._context.get('recuring') == 0:
            if self.tenancy_id.main_cost:
                inv_values.update({
                    'invoice_line_ids': [(0, 0, inv_line_values),
                                         (0, 0, inv_line_main)]
                })
        acc_id = self.env['account.invoice'].create(inv_values)
        self.write({'invc_id': acc_id.id, 'inv': True})
        context = dict(self._context or {})
        wiz_form_id = self.env['ir.model.data'].get_object_reference(
            'account', 'invoice_form')[1]

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

    @api.multi
    def open_invoice(self):
        """
        Description:
            This method is used to open invoce which is created.
        
        Decorators:
            api.multi
        """
        context = dict(self._context or {})
        wiz_form_id = self.env['ir.model.data'].get_object_reference(
            'account', 'invoice_form')[1]
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


class account_payment(models.Model):
    _inherit = 'account.payment'

    @api.multi
    def post(self):
        """
        Description:
            This method ovride base method for when invoice fully paid
            the paid /posted field will be true. and if we pending half
            payment then remaing amount should be shown as pemding amount.
        Decorators:
            api.multi
        """
        res = super(account_payment, self).post()
        if self._context.get('asset') or self._context.get('openinvoice'):
            tenancy = self.env['account.analytic.account']
            for data in tenancy.rent_schedule_ids.browse(
                    self._context.get('active_id')):
                if data:
                    tenan_rent_obj = self.env['tenancy.rent.schedule'].search(
                        [('invc_id', '=', data.id)])
                    amt = 0.0
                    for data1 in tenan_rent_obj:
                        if data1.invc_id.state == 'paid':
                            data1.paid = True
                            data1.move_check = True
                        if data1.invc_id:
                            amt = data1.invc_id.residual
                        data1.write({'pen_amt': amt})
        return res


class PropertyUtility(models.Model):
    _name = "property.utility"

    note = fields.Text(
        string='Remarks')
    ref = fields.Char(
        string='Reference',
        size=60)
    expiry_date = fields.Date(
        string='Expiry Date')
    issue_date = fields.Date(
        string='Issuance Date')
    utility_id = fields.Many2one(
        comodel_name='utility',
        string='Utility')
    property_id = fields.Many2one(
        comodel_name='account.asset.asset',
        string='Property')
    tenancy_id = fields.Many2one(
        comodel_name='account.analytic.account',
        string='Tenancy')
    contact_id = fields.Many2one(
        comodel_name='tenant.partner',
        string='Contact',
        domain="[('tenant', '=', True)]")


class PropertySafetyCertificate(models.Model):
    _name = "property.safety.certificate"

    ew = fields.Boolean(
        'EW')
    weeks = fields.Integer(
        'Weeks')
    ref = fields.Char(
        'Reference',
        size=60)
    expiry_date = fields.Date(
        string='Expiry Date')
    name = fields.Char(
        string='Certificate',
        size=60,
        required=True)
    property_id = fields.Many2one(
        comodel_name='account.asset.asset',
        string='Property')
    contact_id = fields.Many2one(
        comodel_name='tenant.partner',
        string='Contact',
        domain="[('tenant', '=', True)]")


class PropertyAttachment(models.Model):
    _name = 'property.attachment'

    doc_name = fields.Char(
        string='Filename')
    expiry_date = fields.Date(
        string='Expiry Date')
    contract_attachment = fields.Binary(
        string='Attachment')
    name = fields.Char(
        string='Description',
        size=64,
        requiered=True)
    property_id = fields.Many2one(
        comodel_name='account.asset.asset',
        string='Property')


class SaleCost(models.Model):
    _name = "sale.cost"
    _order = 'date'

    @api.one
    @api.depends('move_id')
    def _get_move_check(self):
        self.move_check = bool(self.move_id)

    date = fields.Date(
        string='Date')
    amount = fields.Float(
        string='Amount')
    name = fields.Char(
        string='Description',
        size=100)
    payment_details = fields.Char(
        string='Payment Details',
        size=100)
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency')
    move_id = fields.Many2one(
        comodel_name='account.move',
        string='Purchase Entry')
    sale_property_id = fields.Many2one(
        comodel_name='account.asset.asset',
        string='Property')
    remaining_amount = fields.Float(
        string='Remaining Amount',
        help='Shows remaining amount in currency')
    move_check = fields.Boolean(
        string='Posted',
        compute='_get_move_check',
        method=True,
        store=True)
    rmn_amnt_per = fields.Float(
        string='Remaining Amount In %',
        help='Shows remaining amount in Percentage')
    invc_id = fields.Many2one(
        comodel_name='account.invoice',
        string='Invoice')

    @api.multi
    def create_invoice(self):
        """
        This button Method is used to create account invoice.
        @param self: The object pointer
        """
        if not self.sale_property_id.customer_id:
            raise Warning(_('Please Select Customer'))
        if not self.sale_property_id.income_acc_id:
            raise Warning(_('Please Configure Income Account from Property'))
        account_jrnl_obj = self.env['account.journal'].search(
            [('type', '=', 'sale')])

        inv_line_values = {
            'origin': 'Sale.Cost',
            'name': 'Purchase Cost For'+''+self.sale_property_id.name,
            'price_unit': self.amount or 0.00,
            'quantity': 1,
            'account_id': self.sale_property_id.income_acc_id.id,
        }

        inv_values = {
            'payment_term_id': self.sale_property_id.payment_term.id or False,
            'partner_id': self.sale_property_id.customer_id.id or False,
            'type': 'out_invoice',
            'property_id': self.sale_property_id.id or False,
            'invoice_line_ids': [(0, 0, inv_line_values)],
            'date_invoice': datetime.now().strftime(
                DEFAULT_SERVER_DATE_FORMAT) or False,
            'journal_id': account_jrnl_obj.id or False,
        }
        acc_id = self.env['account.invoice'].create(inv_values)
        self.write({'invc_id': acc_id.id, 'move_check': True})
        context = dict(self._context or {})
        wiz_form_id = self.env['ir.model.data'].get_object_reference(
            'account', 'invoice_form')[1]
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

    @api.multi
    def open_invoice(self):
        """
        This Method is used to Open invoice
        @param self: The object pointer
        """
        context = dict(self._context or {})
        wiz_form_id = self.env['ir.model.data'].get_object_reference(
            'account', 'invoice_form')[1]
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
