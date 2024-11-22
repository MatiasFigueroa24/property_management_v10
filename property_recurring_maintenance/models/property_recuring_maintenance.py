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


class MaintenanceType(models.Model):
    _inherit = 'maintenance.type'

    main_cost = fields.Boolean(
        string='Recurring cost',
        help='Check if the recuring cost involve')
    cost = fields.Float(
        string='Maintenance Cost',
        help='insert the cost')


class MaintenanaceCost(models.Model):
    _name = 'maintenance.cost'

    maint_type = fields.Many2one(
        comodel_name='maintenance.type',
        string='Maintenance Type')
    cost = fields.Float(
        string='Maintenance Cost',
        help='insert the cost')
    tenancy = fields.Many2one(
        comodel_name='account.analytic.account',
        string='Tenancy')

    @api.onchange('maint_type')
    def onchange_property_id(self):
        """
        This Method is used to set maintenance type related fields value,
        on change of property.
        -----------------------------------------------------------------
        @param self: The object pointer
        """
        for data in self:
            if data.maint_type:
                data.cost = data.maint_type.cost or 0.00


class AccountAnalyticAccount(models.Model):
    _inherit = "account.analytic.account"
    _order = 'ref'

    @api.multi
    @api.depends('cost_id')
    def _total_cost_maint(self):
        """
        This method is used to calculate total maintenance
        boolean field accordingly to current Tenancy.
        --------------------------------------------------
        @param self: The object pointer
        """
        total = 0
        for data in self:
            for data_1 in data.cost_id:
                total += data_1.cost
            data.main_cost = total

    cost_id = fields.One2many(
        comodel_name='maintenance.cost',
        inverse_name='tenancy',
        string='cost')
    main_cost = fields.Float(
        string='Maintenance Cost',
        default=0.0,
        compute='_total_cost_maint',
        help="insert maintenance cost")
    recurring = fields.Boolean(
        'Recurring',
        default=True)
