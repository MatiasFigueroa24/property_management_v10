# -*- coding: utf-8 -*-
############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011-Today Serpent Consulting Services PVT LTD.
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
#
############################################################################
{
    'name': 'Property Penalty',
    'version': '1.1',
    'category': 'Real Estate',
    'sequence': 3,
    'description': """
        Property Penalty Management System:

        This module gives the features for penalty calculation On Tenancy rent,
    """,
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'website': 'http://www.serpentcs.com',
    'depends': ['property_management'],
    'demo': [],
    'data': [
        "data/tenancy_schedular.xml",
        "views/property_penalty_view.xml"
    ],
    'auto_install': False,
    'installable': True,
    'application': True,
}
