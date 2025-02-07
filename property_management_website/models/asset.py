# -*- coding: utf-8 -*-
###############################################################################
#
# 	OpenERP, Open Source Management Solution
# 	Copyright (C) 2011-Today Serpent Consulting Services PVT LTD
#    (<http://www.serpentcs.com>)
# 	This program is free software: you can redistribute it and/or modify
# 	it under the terms of the GNU Affero General Public License as
# 	published by the Free Software Foundation, either version 3 of the
# 	License, or (at your option) any later version.
#
# 	This program is distributed in the hope that it will be useful,
# 	but WITHOUT ANY WARRANTY; without even the implied warranty of
# 	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# 	GNU Affero General Public License for more details.
#
# 	You should have received a copy of the GNU Affero General Public License
# 	along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from odoo import models, fields, api
from odoo.tools.translate import _
import logging
from odoo.addons.payment.models.payment_acquirer import ValidationError

_logger = logging.getLogger(__name__)


class account_asset_asset(models.Model):
    _inherit = 'account.asset.asset'
    _description = 'Asset'

    suggested_property_ids = fields.Many2many(
        'property.suggested', 'rel_suggested_property', 'property_id', 'suggested_id', 'Suggested Properties')

    @api.multi
    def _check_secondary_photo(self):
        account_assets_obj = self
        property_photo_true = []
        for one_photo_obj in account_assets_obj.property_photo_ids:
            one_property_photo_obj_true = one_photo_obj.secondary_photo
            property_photo_true.append(one_property_photo_obj_true)
        if property_photo_true.count(True) > 1:
            return False
        return True

    _constraints = [
        (_check_secondary_photo, 'Error!\nSecondary photo is filled if you are change photo please remove first one.', [
            'property_photo_ids']),
    ]


class property_suggested(models.Model):
    _name = "property.suggested"

    other_property_id = fields.Many2one('account.asset.asset', 'Property')
    property_id = fields.Many2one('account.asset.asset', 'Property')


class property_photo(models.Model):
    _inherit = "property.photo"

    secondary_photo = fields.Boolean(
        'Secondary Photo', help='Show photo on website Hover.')


class TxPaypal(models.Model):
    _inherit = 'payment.transaction'

    @api.model
    def _paypal_form_get_tx_from_data(self, data):
        reference, txn_id = data.get('new_transaction_name'), data.get('txn_id')
        if not reference or not txn_id:
            error_msg = _('Paypal: received data with missing reference (%s) or txn_id (%s)') % (reference, txn_id)
            _logger.info(error_msg)
            raise ValidationError(error_msg)

        # find tx -> @TDENOTE use txn_id ?
        txs = self.env['payment.transaction'].search([('reference', '=', reference)])
        if not txs or len(txs) > 1:
            error_msg = 'Paypal: received data for reference %s' % (reference)
            if not txs:
                error_msg += '; no order found'
            else:
                error_msg += '; multiple order found'
            _logger.info(error_msg)
            raise ValidationError(error_msg)
        return self.browse(txs[0])
