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


class PropertyRecurringTestCase(common.TransactionCase):

    def setup(self):
        super(PropertyRecurringTestCase, self).setup()

    def test_recurring_maintenance(self):
        self.details = self.browse_ref(
            'property_management.property_tenancy_t0')
        self.property_id = self.browse_ref('property_management.property_8')
        self.tenant_id = self.browse_ref('property_management.tenant2')
        self.rent_type = self.browse_ref("property_management.rent_type1")
        self.maint1 = self.browse_ref(
            'property_recurring_maintenance.maintenance_type6')
        self.maint2 = self.browse_ref(
            'property_recurring_maintenance.maintenance_type7')
        self.recurring1 = {
            'maint_type': self.maint1.id,
        }
        self.recurring2 = {
            'maint_type': self.maint2.id,
        }

        self.tenancy = self.env['account.analytic.account'].sudo().create(
            {
                'name': 'Tenancy for Radhika Recidency',
                'property_id': self.property_id.id,
                'state': 'draft',
                'is_property': True,
                'tenant_id': self.tenant_id.id,
                'deposit': 5000.00,
                'rent': 8000.00,
                'rent_entry_chck': False,
                'date_start': '07/17/2016',
                'date': '07/07/2017',
                'rent_type_id': self.rent_type.id,
                'cost_id': [(0, 0, self.recurring1),
                            (0, 0, self.recurring2)],
            })
        self.tenancy.cost_id.onchange_property_id()
        self.tenancy._total_cost_maint()
        self.tenancy.button_start()
        self.tenancy.create_rent_schedule()
        self.tenancy.rent_schedule_ids[0].create_invoice()
