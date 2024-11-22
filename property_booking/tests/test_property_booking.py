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
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class PropertyBookingTestCase(common.TransactionCase):

    def setup(self):
        super(PropertyBookingTestCase, self).setup()

    def test_property_booking(self):
        # Property Created
        self.property_type = self.browse_ref(
            'property_management.property_type2')
        self.partner = self.browse_ref('base.res_partner_2')
        self.property_demo = self.browse_ref("property_management.property1")
        self.booking = self.env['property.created'].sudo().create(
            {
                'is_sub_property': True,
                'name': 'Radhika Recidency Booking',
                'parent_id':  self.property_demo.id,
                'category_id': self.property_demo.category_id.id,
                'property_manager': self.property_demo.property_manager.id,
                'type_id': self.property_type.id,
                'prefix3': '2',
                'floor': 5,
                'value': 1500000.00,
                'no_of_property': 4,
            }
        )
        self.booking.create_property()
