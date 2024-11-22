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
from odoo import api, fields, models


class property_per_location_report(models.AbstractModel):
    _name = "report.property_management.report_property_per_location1"

    def property_location(self, data, state):
        property_obj = self.env['account.asset.asset']

        if not data:
            if state and state.id:
                domain = [('state_id', '=', state.id)]
            else:
                domain = []
        elif data:
            domain = [('state_id', '=', data['state_id'][0])]

        property_ids = property_obj.search(domain)
        property_list = []
        sub_property_list = []
        for property_data in property_obj.browse(property_ids.ids):
            if property_data.child_ids:
                for sub in property_data.child_ids:
                    sub_property_list.append(sub.id)
                    property_dict = {
                        'name': property_data.name,
                        'child_ids': sub.name,
                        'city': sub.city,
                        'state_id': property_data.state_id.name,
                        'township': sub.township
                    }
                    property_list.append(property_dict)
            else:
                if property_data.id not in sub_property_list:
                    property_dict = {
                        'name': property_data.name,
                        'child_ids': False,
                        'city': property_data.city,
                        'state_id': property_data.state_id.name,
                        'township': property_data.township
                    }
                    property_list.append(property_dict)
        return property_list

    @api.model
    def render_html(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(
            self.env.context.get('active_ids', []))

        state_id = data.get('state_id')[0]

        detail_res = self.with_context(
            data.get('used_context', {})).property_location(data, state_id)
        docargs = {
            'doc_ids': docids,
            'doc_model': self.model,
            'data': data,
            'docs': docs,
            'property_location': detail_res,
        }
        return self.env['report'].render(
            'property_management.report_property_per_location1', docargs)
