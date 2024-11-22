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


class PropertyMultipleTentTestCase(common.TransactionCase):

    def setup(self):
        super(PropertyMultipleTentTestCase, self).setup()

    def test_property_multiple(self):
        self.details = self.browse_ref(
            'property_management.property_tenancy_t0')
        self.property_id1 = self.browse_ref('property_management.property3')
        self.property_id2 = self.browse_ref('property_management.property1')
        self.tenant_id = self.browse_ref('property_management.tenant2')
        self.rent_type = self.browse_ref("property_management.rent_type1")
        self.multiple_prop1 = {
            'property_ids': self.property_id1.id,
            'ground': 8000.0
        }
        self.multiple_prop2 = {
            'property_ids': self.property_id2.id,
            'ground': 12000.0
        }
        self.tenancy = self.env['account.analytic.account'].sudo().create(
            {
                'name': 'Tenancy for Radhika Recidency',
                'multi_prop': True,
                'state': 'draft',
                'is_property': True,
                'tenant_id': self.tenant_id.id,
                'deposit': 5000.00,
                'rent': 8000.00,
                'rent_entry_chck': False,
                'date_start': '07/17/2016',
                'date': '07/07/2017',
                'rent_type_id': self.rent_type.id,
                'prop_id': [(0, 0, self.multiple_prop1),
                            (0, 0, self.multiple_prop2)],
            })
        self.tenancy._total_prop_rent()
        self.tenancy.button_start()
        self.tenancy.create_rent_schedule()
        self.tenancy.rent_schedule_ids[0].create_invoice()
