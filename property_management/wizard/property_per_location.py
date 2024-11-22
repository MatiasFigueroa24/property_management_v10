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


class property_per_location(models.TransientModel):
    _name = 'property.per.location'

    state_id = fields.Many2one(
        comodel_name='res.country.state',
        string='State')

    @api.multi
    def print_report(self):
        for data1 in self:
            data = data1.read([])[0]
        return self.env['report'].get_action(self, 'property_management.report_property_per_location1',  data=data)
