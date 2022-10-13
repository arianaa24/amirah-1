# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import logging
    
class Location(models.Model):
    _inherit = "stock.location"
    
    productos_sitio_web = fields.Boolean('¿Tomar en cuenta productos para sitio web?', default=False, help="Tomar en cuenta los productos en esta ubicación para las existencias de la tienda en línea.")