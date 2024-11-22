# -*- coding: utf-8 -*-
###############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011-2013 Serpent Consulting Services PVT LTD
#    (<http://www.serpentcs.com>)
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
#
###############################################################################

from odoo import models, fields, api
from odoo import SUPERUSER_ID
from odoo.tools.translate import _


class website_setting(models.Model):
    _name = 'website.setting'

    name = fields.Binary('Image')


class crm_lead_ext(models.Model):
    _inherit = "crm.lead"

    phone_type = fields.Selection([('mob', 'Mobile'), ('work', 'Work'),
                                   ('home', 'Home')], 'Phone Type')
    when_to_call = fields.Selection([
        ('anytime', 'Anytime'),
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('evening', 'Evening')], 'When to Call?')
    property_id = fields.Many2one('account.asset.asset', 'Property')


class res_partner_ext(models.Model):
    _inherit = "res.partner"

    fav_assets_ids = fields.Many2many(
        'account.asset.asset', 'account_asset_partner_rel', 'partner_id', 'asset_id', string='Favorite Property')


class website(models.Model):
    _inherit = 'website'

    def get_fav_property(self):
        user = self.env['res.users'].browse(SUPERUSER_ID)
        for partner in user:
            partner_id = partner.partner_id
        partner_dic = partner_id.read(['fav_assets_ids'])[0]
        fav_assets = len(partner_dic.get('fav_assets_ids')) or 0
        return fav_assets
