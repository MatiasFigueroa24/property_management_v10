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
from odoo.tests import common


class PropertyAppreciationTestCase(common.TransactionCase):

    def setup(self):
        super(PropertyAppreciationTestCase, self).setup()

    def test_property_action(self):
        self.property_type = self.env.ref('property_management.property_type1')
        self.partner = self.env.ref('base.res_partner_2')
        self.property_demo = self.browse_ref("property_management.property1")
        self.rent_type = self.browse_ref("property_management.rent_type1")
        self.asset = self.env['account.asset.asset']
        self.asset_id = self.asset.create(
            {
                'name': 'Radhika Recidency',
                'state': self.property_demo.state,
                'type_id': self.property_type,
                'street': self.property_demo.street,
                'city': self.property_demo.city,
                'country_id': self.property_demo.country_id.id,
                'state_id': self.property_demo.state_id.id,
                'zip': self.property_demo.zip,
                'age_of_property': self.property_demo.age_of_property,
                'category_id': self.property_demo.category_id.id,
                'value': self.property_demo.value,
                'value_residual': self.property_demo.value_residual,
                'ground_rent': self.property_demo.ground_rent,
                'sale_price': self.property_demo.sale_price,
                'furnished': self.property_demo.furnished,
                'facing': self.property_demo.facing,
                'type_id': self.property_demo.type_id.id,
                'floor': self.property_demo.floor,
                'bedroom': self.property_demo.bedroom,
                'bathroom': self.property_demo.bathroom,
                'parent_id': self.property_demo.parent_id,
                'property_manager': self.property_demo.property_manager.id,
                'income_acc_id': self.property_demo.income_acc_id.id,
                'expense_account_id': self.property_demo.expense_account_id.id,
                'rent_type_id': self.rent_type.id,
                'gfa_meter': 11.15,
                'gfa_feet': 120.00,
                'unit_price': 18000.00,
                'appr_salvage_value': 50000.00
            }
        )
        self.asset_id.unit_price_calc()
        self.asset_id._amount_residuals()
        self.asset_id.compute_appreciation_board()
