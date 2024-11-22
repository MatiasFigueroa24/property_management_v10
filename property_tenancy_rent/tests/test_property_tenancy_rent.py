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
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class PropertyTenancyRent(common.TransactionCase):

    def setup(self):
        super(PropertyTenancyRent, self).setup()

    def test_property_action(self):
        # Tenancy/Tenancy Rent Schedule
        self.partner = self.env.ref('base.res_partner_2')
        self.property_demo = self.browse_ref("property_management.property3")
        self.rent_type = self.browse_ref("property_management.rent_type1")
        self.date_today = datetime.today()
        self.tenancy = self.env['account.analytic.account'].sudo().create(
            {
                'name': 'Tenancy for Glohork Villa',
                'prop_ids': self.property_demo.id,
                'state': 'draft',
                'is_tenancy_rent': True,
                'property_owner_id': self.partner.id,
                'deposit': 5000.00,
                'rent': 8000.00,
                'rent_entry_chck': False,
                'date_start': datetime.today(),
                'date': datetime.today(),
            })
        self.cur = self.browse_ref('base.in')
        self.rent = self.env['tenancy.rent.schedule'].sudo().create(
            {
                'start_date': datetime.today(),
                'amount': 8000.00,
                'currency_id': self.cur.id,
            })
