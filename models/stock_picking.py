# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import logging

class Picking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        rec = super(Picking, self).button_validate()
        if self.move_ids_without_package:
            for linea in self.move_ids_without_package:
                cantidades = linea.product_id._product_available()
                if cantidades[linea.product_id.id]['virtual_available'] <= 0:
                    linea.product_id.website_published = False
        return rec
