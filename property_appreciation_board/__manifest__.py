# -*- coding: utf-8 -*-
###############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011-Today Serpent Consulting Services PVT LTD
#    (<http://www.serpentcs.com>)
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
###############################################################################
{
    'name': 'Property Appreciation Board',
    'version': '2.0',
    'category': 'Real Estate',
    'description': """
    Property Management System

    Odoo Property Management System will help you to manage your real estate
    portfolio with Property valuation, Maintenance, Insurance, Utilities and
    Rent management with reminders for each KPIs. ODOO's easy to use Content
    management system help you to display available property on website with
    its gallery and other details to reach easily to end users. With the help
    of inbuilt Business Intelligence system it will be more easy to get various
    analytical reports and take strategical decisions.
     """,
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'website': 'http://www.serpentcs.com',
    'depends': ['property_management'],
    'data': ['security/ir.model.access.csv',
             'views/property_appreciation_board_view.xml',
             ],
    'auto_install': False,
    'installable': True,
    'application': True,
}
