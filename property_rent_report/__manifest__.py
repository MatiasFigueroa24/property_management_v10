# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2016 Serpent Consulting Services Pvt. Ltd.
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
##############################################################################
{
    "name": "Property Rent Payment Voucher Report",
    "version": "1.0",
    "author": "Serpent Consulting Services Pvt. Ltd",
    "website": "http://www.serpentcs.com",
    "description": """
Make report on payment receipt
""",
    'depends': ['property_management', 'analytic', ],
    'data': [
        'views/report_property_rent_templates.xml',
        'views/report_configuration_view.xml'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
