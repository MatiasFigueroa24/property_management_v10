# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011-Till Today Serpent Consulting Services PVT LTD (<http://www.serpentcs.com>)
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
#
############################################################################
{
    'name': 'Property Management Website',
    'description': 'This module will help you to manage your real estate portfolio with Property valuation, Maintenance, Insurance, Utilities and Rent management with reminders for each KPIs.',
    'category': 'Website',
    'version': '1.0',
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'depends': ['property_management', 'website', 'base_geolocalize', 'payment_paypal', 'property_penalty'],
    'data': [
        'security/webiste_pms_security.xml',
        'security/ir.model.access.csv',
        'data/website_data.xml',
        'data/website_data_no_update.xml',
        'view/template.xml',
        # 'view/assets.xml',
        # 'view/asset_view.xml',
    ],
    'application': True,
    'installable': True,
}
