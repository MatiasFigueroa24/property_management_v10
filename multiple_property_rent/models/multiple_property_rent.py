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


class Recurring(models.Model):
    _name = 'property.rent'

    property_ids = fields.Many2one(
        comodel_name='account.asset.asset',
        string='Property',
        help='Property name')
    ground = fields.Float(
        string='Ground Rent',
        help='Rent of property', )
    ten = fields.Many2one(
        comodel_name='account.analytic.account',
        string='Ten')

    @api.onchange('property_ids')
    def ground_rent(self):
        """
        This method is used to get rent when select the property
        """
        val = 0.0
        if self.property_ids:
            val = float(self.property_ids.ground_rent)
        self.ground = val


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    # @api.one
    @api.onchange('prop_id', 'multi_prop')
    def _total_prop_rent(self):
        """
        This method calculate total rent of all the selected property.
        @param self: The object pointer
        """
        tot = 0.00
        if self._context.get('is_tenancy_rent'):
            prop_val = self.prop_ids.ground_rent or 0.0
        else:
            prop_val = self.property_id.ground_rent or 0.0
        for pro_record in self:
            if self.multi_prop:
                for prope_ids in pro_record.prop_id:
                    tot += prope_ids.ground
                pro_record.rent = tot + prop_val
            else:
                pro_record.rent = prop_val

    prop_id = fields.One2many(
        comodel_name='property.rent',
        inverse_name='ten',
        string="Property")
    # rent = fields.Float(
    #     string='Rent',
    #     # compute='_total_prop_rent',
    #     # readonly=True,
    #     store=True)
    multi_prop = fields.Boolean(
        string='Multiple Property',
        help="Check this box Multiple property.")

    @api.onchange('multi_prop')
    def onchange_multi_prop(self):
        """
        If the context is get is_tenanacy_rent then property id is 0
        or if get than prop_ids is zero
        @param self: The object pointer
        """
        if self.multi_prop is True:
            if not self._context.get('is_tenancy_rent'):
                self.property_id = 0
            elif self._context.get('is_tenancy_rent'):
                self.prop_ids = 0
