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


class PropertyCommissionTestCase(common.TransactionCase):

    def setup(self):
        super(PropertyCommissionTestCase, self).setup()

    def test_commission(self):
        self.details = self.browse_ref(
            'property_management.property_tenancy_t0')
        self.property_id = self.browse_ref('property_management.property3')
        self.tenant_id = self.browse_ref('property_management.tenant2')
        self.rent_type = self.browse_ref("property_management.rent_type1")
        self.agent = self.env['res.partner'].sudo().create(
            {
                'name': 'Patel Kapil',
                'agent': True,
                'email': 'patel@yourcompany.com'
            })

        self.tenancy = self.env['account.analytic.account'].sudo().create(
            {
                'name': 'Tenancy for Radhika Recidency',
                'property_id': self.property_id.id,
                'state': 'draft',
                'is_property': True,
                'commission': True,
                'agent': self.agent.id,
                'tenant_id': self.tenant_id.id,
                'commission_type': 'fixed',
                'fix_qty': 10.00,
                'deposit': 5000.00,
                'rent': 8000.00,
                'date_start': '07/17/2016',
                'date': '07/07/2017',
                'rent_type_id': self.rent_type.id,
            })
        self.tenancy.button_start()
        self.tenancy.create_rent_schedule()
        self.tenancy.calculate_commission()
        self.tenancy.create_commission()
