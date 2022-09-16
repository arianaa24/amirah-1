# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import logging

class Website(models.Model):
    _inherit = "website"
    
    def existencias(self, producto):
        ubicaciones = 0
        existencias = ''
        mensaje = ''
        cantidades = self.env['stock.quant'].search([('quantity','>',0),('product_id.id','=',producto)])
        for quant in cantidades:
            if ubicaciones < 2:
                if quant.location_id.warehouse_id:
                    tienda = quant.location_id.warehouse_id.name
                else:
                    tienda = quant.location_id.name
                ubicaciones += 1
                existencias += str(tienda) + ': ' + str(quant.available_quantity) + ' unidades. '
        if existencias:
            mensaje = 'Existencias: ' + existencias
        logging.warning(mensaje)
        return mensaje

    def producto_agotado(self,productos, attribute=None):
        agotado = True
        #ubicacion_id = self.env['website'].get_current_website().warehouse_id.lot_stock_id
        cantidades = self.env['stock.quant'].search([('quantity','>',0),('product_id','in',productos.ids)])
        cantidad = 0
        for quant in cantidades:
            if attribute:
                if attribute.id in quant.product_id.product_template_variant_value_ids.ids:
                    cantidad += quant.available_quantity
            else:
                cantidad += quant.available_quantity
        if cantidad and cantidad > 0:
            agotado = False
        if attribute.attribute_id.create_variant == 'no_variant':
            agotado = False
        return agotado

    def _actualizar_producto(self):
        producto_template_ids=self.env['product.template'].search([])
        if producto_template_ids:
            for pt in producto_template_ids:
                productos_activos = pt._get_possible_variants()
                producto_agotado = self.producto_agotado(productos_activos)
                logging.warning(pt.name + 'agotado: ' + str(producto_agotado))
                if producto_agotado == True:
                    pt.website_published = False
                else:
                    pt.website_published = True
                logging.warning(pt.name + ' Publicado: ' + str(pt.website_published))
                    
    # def producto_agotado(self,productos, attribute=None):
    #     res = {'agotado': True, 'almacenes':[]}
    #     agotado = True
    #     #ubicacion_id = self.env['website'].get_current_website().warehouse_id.lot_stock_id
    #     cantidades = self.env['stock.quant'].search([('quantity','>',0),('product_id','in',productos.ids)])
    #     cantidad = 0
    #     for quant in cantidades:
    #         #if quant.location_id.warehouse_id:
                
    #         logging.warning(quant.location_id.warehouse_id.name)
    #         if attribute:
    #             if attribute.name in quant.display_name:
    #                 cantidad = quant.available_quantity
    #         else:
    #             cantidad += quant.available_quantity
    #     if cantidad and cantidad> 0:
    #         res['agotado'] = False
    #         agotado = False
    #     return res

    # def _actualizar_producto(self):
    #     producto_template_ids=self.env['product.template'].search([])
    #     if producto_template_ids:
    #         for pt in producto_template_ids:
    #             productos_activos = pt._get_possible_variants()
    #             producto_agotado = self.producto_agotado(productos_activos)
    #             if producto_agotado['agotado'] == True:
    #                 pt.website_published = False
    #             else:
    #                 pt.website_published = True