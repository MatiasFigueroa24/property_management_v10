# -*- encoding: utf-8 -*-
##############################################################################
#
#	OpenERP, Open Source Management Solution
#	Copyright (C) 2012-Today Serpent Consulting Services Pvt. Ltd. (<http://www.serpentcs.com>)
#	Copyright (C) 2004 OpenERP SA (<http://www.openerp.com>)
#
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

from datetime import datetime
from odoo.tools import misc
from odoo.exceptions import Warning, ValidationError
from odoo import models, fields, api, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class wizard_renew_tenancy(models.TransientModel):
    _name = 'renew.tenancy'

    start_date = fields.Date(
        string='Start Date')
    end_date = fields.Date(
        string='End Date')
    rent_type_id = fields.Many2one(
        comodel_name='rent.type',
        string='Rent Type',
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
    def renew_contract(self):
        """
                This Button Method is used to Renew Tenancy.
        @param self: The object pointer
        @return: Dictionary of values.
        """
        cr, uid, context = self.env.args
        context = dict(context)
        if context is None:
            context = {}
        modid = self.env['ir.model.data'].get_object_reference(
            'property_management', 'property_analytic_view_form')
        if context.get('active_ids', []):
            for rec in self:
                start_d = datetime.strptime(
                    rec.start_date, DEFAULT_SERVER_DATE_FORMAT).date()
                end_d = datetime.strptime(
                    rec.end_date, DEFAULT_SERVER_DATE_FORMAT).date()
                if start_d > end_d:
                    raise Warning(
                        _('Please Insert End Date Greater Than Start Date'))
                act_prop = self.env['account.analytic.account'].browse(
                    context['active_ids'])
                act_prop.write({
                    'date_start': rec.start_date,
                    'date': rec.end_date,
                    'rent_type_id': rec.rent_type_id and rec.rent_type_id.id or False,
                    'state': 'draft',
                    'rent_entry_chck': False,
                })
        self.env.args = cr, uid, misc.frozendict(context)
        return {
            'view_mode': 'form',
            'view_id': modid[1],
            'view_type': 'form',
            'res_model': 'account.analytic.account',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'res_id': context['active_ids'][0],
        }
