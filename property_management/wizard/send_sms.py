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
import datetime
import urllib
from odoo import tools
from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class tenant_sms_send(models.TransientModel):
    _name = "tenant.sms.send"
    _description = "Send SMS"

    user = fields.Char(
        string='Login',
        size=256,
        required=True)
    password = fields.Char(
        string='Password',
        size=256,
        required=True)

    @api.multi
    def sms_send(self):
        """
        This is used to sending sms through bulk sms api
        """
        partner_pool = self.env['tenancy.rent.schedule']
        active_ids = partner_pool.search([('start_date', '<', datetime.date.today(
        ).strftime(DEFAULT_SERVER_DATE_FORMAT)), ('paid', '=', False)])
        partners = partner_pool.browse(active_ids.ids)
        for partner in partners:
            if partner.rel_tenant_id.parent_id:
                if partner.rel_tenant_id.parent_id[0].mobile:
                    for data in self:
                        # bulksms API is used for messege sending
                        urllib.urlopen('''http://bulksms.vsms.net:5567/eapi/submission/send_sms/2/2.0?username=%s&password=%s&message=Hello Mr %s,\nYour rent QAR %d of %s is unpaid so kindly pay as soon as possible.\nRegards,\nProperty management firm.&msisdn=%s''' % (
                            data.user, data.password, partner.rel_tenant_id.name, partner.amount, partner.start_date, partner.rel_tenant_id.parent_id[0].mobile))
        return {'type': 'ir.actions.act_window_close'}
