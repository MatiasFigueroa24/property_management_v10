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


class property_finance_report(models.Model):
    _name = "property.finance.report"
    _auto = False

    type_id = fields.Many2one('property.type', 'Property Type')
    date = fields.Date('Purchase Date')
    parent_id = fields.Many2one('account.asset.asset', 'Parent Property')
    name = fields.Char("Parent Property")
    purchase_price = fields.Float('Purchase Price')

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        obj = cr.execute("""CREATE or REPLACE VIEW property_finance_report as SELECT id,name,type_id,purchase_price,date
			FROM account_asset_asset""" )
