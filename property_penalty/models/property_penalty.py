# -*- coding: utf-8 -*-
###############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011-Today Serpent Consulting Services PVT LTD.
#    (<http://www.serpentcs.com>)
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
###############################################################################
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.exceptions import Warning
from openerp.tools import misc


class AccountAnalyticAccount(models.Model):
    _inherit = "account.analytic.account"

    penalty = fields.Float(
        string='Penalty (%)')
    penalty_day = fields.Integer(
        string='Penalty Count After Days')
    penalty_a = fields.Boolean(
        'Penalty',
        default=True)


class TenancyRentSchedule(models.Model):
    _inherit = "tenancy.rent.schedule"
    _rec_name = "tenancy_id"
    _order = 'start_date'

    penalty_amount = fields.Float(
        string='Penalty',
        store=True)

    @api.multi
    def calculate_penalty(self):
        """
        This Method is used to calculate penalty.
        -----------------------------------------
        @param self: The object pointer
        """
        today_date = datetime.today().date()
        for one_payment_line in self:
            if not one_payment_line.paid:
                ten_date = datetime.strptime(
                    one_payment_line.start_date, DEFAULT_SERVER_DATE_FORMAT).date()
                if one_payment_line.tenancy_id.penalty_day != 0:
                    ten_date = ten_date + \
                        relativedelta(
                            days=int(one_payment_line.tenancy_id.penalty_day))
                if ten_date < today_date:
                    if (today_date - ten_date).days:
                        line_amount_day = (
                            one_payment_line.tenancy_id.rent * one_payment_line.tenancy_id.penalty) / 100
                        self.write({'penalty_amount': line_amount_day})
        return True
