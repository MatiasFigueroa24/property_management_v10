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
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil import parser
from odoo import api, fields, models
from odoo.tools import ustr


class tenancy_detail(models.AbstractModel):
    _name = 'report.property_management.report_tenancy_by_property'

    def get_details(self, start_date, end_date, property_id):
        data_1 = []
        tenancy_obj = self.env["account.analytic.account"]
        tenancy_ids = tenancy_obj.search([
            ('property_id', '=', property_id[0]),
            ('date_start', '>=', start_date),
            ('date', '<=', end_date),
            ('is_property', '=', True)])
        for data in tenancy_ids:
            if data.currency_id:
                cur = data.currency_id.symbol
            data_1.append({
                'name': data.name,
                'tenant_id': data.tenant_id.name,
                'date_start': parser.parse(
                    data.date_start).strftime('%m/%d/%Y'),
                'date': parser.parse(data.date).strftime('%m/%d/%Y'),
                'rent': cur + ustr(data.rent),
                'rent_type_id': data.rent_type_id.name,
                'rent_type_month': data.rent_type_id.renttype,
                'state': data.state
            })
        return data_1

    @api.model
    def render_html(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(
            self.env.context.get('active_ids', []))

        start_date = data['form'].get('start_date', fields.Date.today())
        end_date = data['form'].get(
            'end_date', str(datetime.now() + relativedelta(
                months=+1, day=1, days=-1))[:10])
        property_id = data['form'].get('property_id')

        detail_res = self.with_context(
            data['form'].get('used_context', {})).get_details(
            start_date, end_date, property_id)
        docargs = {
            'doc_ids': docids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'time': time,
            'get_details': detail_res,
        }
        docargs['data'].update({'end_date': parser.parse(
            docargs.get('data').get('end_date')).strftime('%m/%d/%Y')})
        docargs['data'].update({'start_date': parser.parse(
            docargs.get('data').get('start_date')).strftime('%m/%d/%Y')})
        return self.env['report'].render(
            'property_management.report_tenancy_by_property', docargs)
