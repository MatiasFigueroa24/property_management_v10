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
from odoo import tools
import datetime
from odoo import models, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class partner_wizard_spam(models.TransientModel):
    _name = "tenant.wizard.mail"
    _description = "Mass Mailing"

    @api.multi
    def mass_mail_send(self):
        """
        This method is used to sending mass mailing to tenant
        for Reminder for rent payment 
        """
        partner_pool = self.env['tenancy.rent.schedule']
        active_ids = partner_pool.search(
            [('start_date', '<', datetime.date.today().strftime(DEFAULT_SERVER_DATE_FORMAT))])
        partners = partner_pool.browse(active_ids.ids)
        for partner in partners:
            if partner.rel_tenant_id.parent_id:
                if partner.rel_tenant_id.parent_id[0].email:
                    to = '"%s" <%s>' % (
                        partner.rel_tenant_id.name, partner.rel_tenant_id.parent_id[0].email)
        # TODO: add some tests to check for invalid email addresses
        # CHECKME: maybe we should use res.partner/email_send
                    tools.email_send(tools.config.get('email_from', False),
                                     [to],
                                     'Reminder for rent payment',
                                     '''
										 Hello Mr %s,\n
										 Your rent QAR %d of %s is unpaid so kindly pay as soon as possible.
										 \n
										 Regards,
										 Administrator.
										 Property management firm.
										 ''' % (partner.rel_tenant_id.name, partner.amount, partner.start_date))
        return {'type': 'ir.actions.act_window_close'}
