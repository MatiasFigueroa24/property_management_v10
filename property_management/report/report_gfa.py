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

from odoo import tools
from odoo import models, fields


class gfa_analysis_report(models.Model):
    _name = "gfa.analysis.report"
    _auto = False

    name = fields.Char('Property Name')
    active = fields.Boolean('Active')
    parent_id = fields.Many2one(
        'account.asset.asset', string='Parent Property')
    type_id = fields.Many2one('property.type', string='Property Type')
    gfa_feet = fields.Float('GFA(Sqft)')
    date = fields.Date('Purchase Date')

    def init(self):
        tools.drop_view_if_exists(self._cr, 'gfa_analysis_report')
        obj = self._cr.execute("""CREATE or REPLACE VIEW gfa_analysis_report as SELECT id,name,active,parent_id,type_id,gfa_feet,date
			FROM account_asset_asset """ )
