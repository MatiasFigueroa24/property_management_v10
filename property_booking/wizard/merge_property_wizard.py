# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011-Today Serpent Consulting Services Pvt. Ltd.
#    (<http://serpentcs.com>).
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
#
##############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import Warning


class MergePropertyWizard(models.TransientModel):
    _name = 'merge.property.wizard'
    _description = 'Merge properties'

    @api.multi
    def merge_property(self):
        """
        This Method is used to merge sub properties
        from Sub Properties menu.
        """
        if self._context is None:
            self._context = {}
        property_obj = self.env['property.created']
        if self._context.get('active_ids', []):
            if len(self._context['active_ids']) <= 1:
                raise Warning(_("Please select atleast two properties."))
            data_prop = []
            for propert_brw in property_obj.browse(self._context['active_ids']
                                                   ):
                data_prop += propert_brw.read(['state',
                                               'parent_id', 'floor_number'])
            for x in data_prop:
                if x['parent_id'] == False:
                    raise Warning(
                        _("Please select sub properties. \n \
                        Not parent property!."))
            states = [x['state'] for x in data_prop if x['state'] != 'draft']
            if states:
                raise Warning(
                    _("Only Available state properties are allowed to be \
                    merged!"))
            parents = list(set([x['parent_id'][0] for x in data_prop]))
            if len(parents) != 1:
                raise Warning(
                    _("Please select sub properties from the same Parent \
                    property!"))
            check_property = False
            maxm = 0
            prop_f_no = 0
            prop_p_no = False
            for prop in property_obj.browse(self._context['active_ids']):
                if not check_property:
                    check_property = prop
                    prop_f_no = int(prop.floor_number)
                    prop_p_no = str(prop.prop_number)
                    maxm = int(prop.label_id.name)
                    continue
                maxm += int(prop.label_id.name)
                vals = {'name': prop.name + "->" + "Merge" + "->" +
                        check_property.name,
                        'state': 'cancel',
                        }
                floor_no = list(set([x['floor_number'][0] for x in data_prop]))
                if len(floor_no) != 1:
                    if int(prop.floor_number) in (prop_f_no + 1,
                                                  prop_f_no - 1) and \
                            str(prop.prop_number) == \
                            prop_p_no:
                        prop.write(vals)
                    else:
                        raise Warning(
                            _("Please select sub properties from \
                            the same Floors!"))
                prop.write(vals)
            requ_id = self.env['property.label'].search(
                [('name', '=', int(maxm))])
            if len(requ_id.ids) != 1 and int(maxm) != 0:
                raise Warning(
                    _('Please Create label of %s ' % (str(maxm) + " " +
                                                      str(prop.label_id.code)))
                )
            check_property.write({'label_id': maxm})
        return {'type': 'ir.actions.act_window_close'}
