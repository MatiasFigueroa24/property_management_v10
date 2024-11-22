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
from odoo import models, fields


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    property_id = fields.Many2one(
        comodel_name='account.asset.asset',
        string='Property')
    is_property = fields.Boolean(
        string='Is Property')
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product',
        domain=[('sale_ok', '=', True)],
        change_default=True,
        ondelete='restrict',
        required=False)
    product_uom = fields.Many2one(
        comodel_name='product.uom',
        string='Unit of Measure',
        required=False)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_property = fields.Boolean(
        string='Is Property',
        default=False)
