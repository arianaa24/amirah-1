# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import logging

class Website(models.Model):
    _inherit = "website"

    def producto_agotado(self,productos, attribute=None):
        agotado = True
        #ubicacion_id = self.env['website'].get_current_website().warehouse_id.lot_stock_id
        cantidades = self.env['stock.quant'].search([('quantity','>',0),('product_id','in',productos.ids)])
        cantidad = 0
        for quant in cantidades:
            if attribute:
                if attribute.name in quant.display_name:
                    cantidad = quant.available_quantity
            else:
                cantidad += quant.available_quantity
                
        if cantidad and cantidad> 0:
            agotado = False
        return agotado

    def _actualizar_producto(self):
        producto_template_ids=self.env['product.template'].search([])
        if producto_template_ids:
            for pt in producto_template_ids:
                productos_activos = pt._get_possible_variants()
                producto_agotado = self.producto_agotado(productos_activos)
                if producto_agotado == True:
                    pt.website_published = False
                else:
                    pt.website_published = True