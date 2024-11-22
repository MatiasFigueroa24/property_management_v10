# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _


class Propietario(models.Model):
    _name = 'property.owner'

    propietario_id = fields.Many2one('res.partner', string="Propietario")
    propiedad_id = fields.Many2one('account.asset.asset', string="Propiedad")
    porcentaje = fields.Float('Porcentaje')

