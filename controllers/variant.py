# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import logging

from odoo.addons.website_sale.controllers.variant import VariantController
import logging

class AmirahVariantController(VariantController):
    
    @http.route(['/sale/get_combination_existencias'], type='json', auth="public")    
    def existencias_controller(self, producto):
        existencias = ''
        mensaje = ''
        cantidades = request.env['stock.quant'].sudo().search([('quantity','>',0),('product_id.id','=',producto),('location_id.productos_sitio_web','=',True)], limit=2)
        for quant in cantidades:
            if quant.location_id.warehouse_id:
                tienda = quant.location_id.warehouse_id.name
            else:
                tienda = quant.location_id.name
            existencias += str(tienda) + ': ' + str(quant.available_quantity) + ' unidades. '
        if existencias:
            mensaje = 'Existencias: ' + existencias
        return mensaje
