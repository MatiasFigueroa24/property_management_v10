# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011-Today Serpent Consulting Services PVT LTD (<http://www.serpentcs.com>)
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
    'name': 'Property Management System',
    'version': '2.14',
    'category': 'Real Estate',
    'sequence': 1,
    'description': """
Property Management System:

Odoo Property Management System will help you to manage your real estate portfolio with Property valuation,
Maintenance, Insurance, Utilities and Rent management with reminders for each KPIs.
ODOO's easy to use Content management system help you to display available property on website with its 
gallery and other details to reach easily to end users. 
With the help of inbuilt Business Intelligence system it will be more easy to get various analytical reports 
and take strategical decisions.
        
     """,
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'website': 'http://www.serpentcs.com',
    'depends': ['base', 'l10n_generic_coa', 'sale_crm', 'account_asset', 'account_voucher', 'document', 'account_budget', 'account', 'analytic', 'web_calendar', 'crm', 'portal', 'account_accountant', 'mail', 'report'],
    'data': [
        'security/pms_security.xml',
        'security/ir.model.access.csv',
        'data/property_schedular.xml',
        'data/property_code_sequence.xml',
        'data/email_template.xml',
        #                'views/templates.xml',
        'views/res_partner.xml',
        'views/property_view.xml',
        'views/asset_view.xml',
        'views/report_account_move_templates.xml',
        'views/account_analytic_view.xml',
        'views/account_view.xml',
        'views/report_property_external_templates.xml',
        'wizard/contract_expiry_report_view.xml',
        'wizard/send_mail_view.xml',
        'wizard/send_sms_view.xml',
        'wizard/tenancy_detail_by_tenant_report_view.xml',
        'wizard/tenancy_detail_property_report_view.xml',
        'wizard/safety_certificate_expiry_view.xml',
        'wizard/income_report_view.xml',
        'wizard/document_expiry_view.xml',
        'wizard/property_per_location.xml',
        'wizard/book_to_available.xml',
        'wizard/crm_make_sale_view.xml',
        'wizard/renew_tenancy_view.xml',
        'views/report_contract_expiry_templates.xml',
        'views/report_property_per_location_templates.xml',
        'views/report_income_expenditure_templates.xml',
        'views/report_safety_certificate_expiry_templates.xml',
        'views/report_document_expiry_templates.xml',
        'views/report_tenancy_detail_by_tenant_templates.xml',
        'views/report_tenancy_detail_by_property_templates.xml',
        'views/property_management_report.xml',
        'views/report_gfa__templates.xml',
        'views/report_operational_cost_templates.xml',
        #                'views/report_investment_templates.xml',
        'views/report_occupancy_performance_templates.xml',
        'security/property_security.xml',
        'views/lead_view.xml',
        'views/sale_view.xml',
        #                'views/property_management.xml',
    ],
    'demo': ['data/account_asset_demo.xml'],
    #    'qweb': ['static/src/xml/property_management.xml'],
    'auto_install': False,
    'installable': True,
    'application': True,
    'price': 200,
    'currency': 'EUR',
}
