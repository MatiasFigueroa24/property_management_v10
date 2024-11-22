# -*- coding: utf-8 -*-
##############################################################################
#
#	OpenERP, Open Source Management Solution
#	Copyright (C) 2011-Today Serpent Consulting Services PVT LTD
#	(<http://www.serpentcs.com>)
#
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU Affero General Public License as
#	published by the Free Software Foundation, either version 3 of the
#	License, or (at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU Affero General Public License for more details.
#
#
#	You should have received a copy of the GNU Affero General Public License
#	along with this program.  If not, see <http://www.gnu.org/licenses/>.
############################################################################

from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class tenancy_tenant_report(models.TransientModel):
    _name = 'tenancy.tenant.report'

    start_date = fields.Date(
        string='Start date',
        required=True)
    end_date = fields.Date(
        string='End date',
        required=True)
    tenant_id = fields.Many2one(
        comodel_name='tenant.partner',
        string='Tenant',
        required=True)

    @api.constrains('start_date', 'end_date')
    def check_date_overlap(self):
        """
        This is a constraint method used to check the from date smaller than
        the Exiration date.
        @param self : object pointer
        """
        for ver in self:
            if ver.start_date and ver.end_date:
                dt_from = datetime.strptime(
                    ver.start_date, DEFAULT_SERVER_DATE_FORMAT)
                dt_to = datetime.strptime(
                    ver.end_date, DEFAULT_SERVER_DATE_FORMAT)
                if dt_to < dt_from:
                    raise ValidationError(
                        'End date should be greater than Start Date!')

    @api.multi
    def open_tanancy_tenant_gantt_view(self):
        """
        This method is used to open record in gantt view between selected dates
        @param self : object pointer
        """
        for data_rec in self:
            data = data_rec.read([])[0]
            start_date = data['start_date']
            end_date = data['end_date']
            tenant_id = data['tenant_id'][0]
            wiz_form_id = self.env['ir.model.data'].get_object_reference(
                'property_management', 'view_analytic_gantt')[1]
            tenancy_ids = self.env["account.analytic.account"].search(
                [('tenant_id', '=', tenant_id), ('date_start', '>=', start_date), ('date_start', '<=', end_date)])
        return {
            'view_type': 'form',
            'view_id': wiz_form_id,
            'view_mode': 'gantt',
            'res_model': 'account.analytic.account',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'context': self._context,
            'domain': [('id', 'in', tenancy_ids.ids)],
        }

    @api.multi
    def open_tanancy_tenant_tree_view(self):
        """
        This method is used to open record in tree view between selected dates
        @param self : object pointer
        """
        for data_rec in self:
            data = data_rec.read([])[0]
            start_date = data['start_date']
            end_date = data['end_date']
            tenant_id = data['tenant_id'][0]
            wiz_form_id = self.env['ir.model.data'].get_object_reference(
                'property_management', 'property_analytic_view_tree')[1]
            tenancy_ids = self.env['account.analytic.account'].search(
                [('tenant_id', '=', tenant_id), ('date_start', '>=', start_date), ('date_start', '<=', end_date)])
        return {'name': 'Tenancy Report By Tenant',
                'view_type': 'tree',
                'view_id': wiz_form_id,
                'view_mode': 'tree',
                'res_model': 'account.analytic.account',
                'type': 'ir.actions.act_window',
                'target': 'current',
                'context': self._context,
                'domain': [('id', 'in', tenancy_ids.ids)],
                }

    @api.multi
    def print_report(self):
        if self._context is None:
            self._context = {}
        partner_obj = self.env['tenant.partner']
        for data_rec in self:
            data = data_rec.read([])[0]
            partner_rec = partner_obj.browse(data['tenant_id'][0])
            data.update({'tenant_name': partner_rec.name})
        data = {
            'ids': self.ids,
            'model': 'tenant.partner',
            'form': data
        }
        return self.env['report'].get_action(self, 'property_management.report_tenancy_by_tenant',
                                             data=data)
