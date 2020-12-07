# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import logging

class Picking(models.Model):
    _inherit = "stock.picking"


    def producto_agotado(self,productos):
        agotado = True
        cantidades = self.env['stock.quant'].search([('location_id','=',self.location_id.id),('quantity','>',0),('product_id','in',productos.ids)])
        if cantidades:
            agotado = False
        return agotado

    def button_validate(self):
        rec = super(Picking, self).button_validate()
        if self.move_ids_without_package:
            for linea in self.move_ids_without_package:
                productos_activos = linea.product_id.product_tmpl_id._get_possible_variants()
                producto_agotado = self.producto_agotado(productos_activos)
                if producto_agotado == True:
                    linea.product_id.website_published = False
        return rec
