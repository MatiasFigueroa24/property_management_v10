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

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    tenant = fields.Boolean(
        string='Tenant',
        help="Check this box if this contact is a tenant.")
    occupation = fields.Char(
        string='Occupation',
        size=20)
    agent = fields.Boolean(
        string='Agent',
        help="Check this box if this contact is a Agent.")
    is_worker = fields.Boolean(
        string='Worker',
        help="Check this box if this contact is a worker.")
    prop_manintenance_ids = fields.One2many(
        comodel_name='property.maintenance',
        inverse_name='assign_to',
        string="Property Maintenance")
    worker_maintenance_ids = fields.Many2many(
        comodel_name='maintenance.type',
        relation='rel_worker_maintenance',
        column1='partner_id',
        column2='maintenance_id',
        string='Maintenance Type',
        help="Select the types of work the worker does.")
    mobile = fields.Char(
        string='Mobile',
        size=15)

    @api.constrains('mobile')
    def _check_value(self):
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
    def _check_values(self):
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


class ResUsers(models.Model):
    _inherit = "res.users"

    tenant_id = fields.Many2one(
        comodel_name='tenant.partner',
        string='Related Tenant')
    tenant_ids = fields.Many2many(
        comodel_name='tenant.partner',
        relation='rel_ten_user',
        column1='user_id',
        column2='tenant_id',
        string='All Tenants')


class ResCompany(models.Model):
    _inherit = 'res.company'

    default_password = fields.Char(
        string='Default Password')
