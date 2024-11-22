# -*- coding: utf-8 -*-
###############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011-Today Serpent Consulting Services PVT LTD
#    (<http://www.serpentcs.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
###############################################################################
from odoo import models, fields, api


class AccountAssetAsset(models.Model):
    _inherit = "account.asset.asset"

    @api.depends('tenancy_property')
    def total_exp_amt_calc(self):
        """
        This method is used to calculate Total income amount.
        --------------------------------------------------------
        @param self: The object pointer
        """
        total = 0.00
        for property_brw in self:
            tenant_ids = self.env['account.analytic.account'].search(
                [('prop_ids', '=', property_brw.id),
                 ('is_tenancy_rent', '=', True)])
            for data in tenant_ids:
                for data1 in data:
                    total += data1.total_deb_cre_amt
            property_brw.total_exp_amt = total

    tenancy_property = fields.One2many(
        'account.analytic.account', 'prop_ids', 'Tenancy Property')
    currenttenant_id = fields.Many2one('tenant.partner', 'Current Tenant')
    total_exp_amt = fields.Float(compute='total_exp_amt_calc',
                                 string='Tenancy Rent Expense',
                                 default=0.0)
