# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import base64
import io
import logging
import xlsxwriter

class WizardReporteInventario(models.TransientModel):
    _name = 'amirah.reporte_inventario'
    
    fecha_hasta = fields.Date('Fecha fin', required=True, default=fields.Datetime.now)
    
    name = fields.Char('Nombre archivo')
    archivo = fields.Binary('Archivo')
    
    def print_report_excel(self):
        for w in self:
            dic = {}
            dic['fecha_hasta'] = w['fecha_hasta']
            
            f = io.BytesIO()
            libro = xlsxwriter.Workbook(f) 
            hoja = libro.add_worksheet('Inventario')
            bold = libro.add_format({'bold': True})
            border = libro.add_format({'border': 1, 'bold': True})
            num_format = libro.add_format({'num_format': 'Q#,##0.00'})
            
            hoja.write(0, 4, 'Al ' + str(dic['fecha_hasta']), bold)
            hoja.write(2, 1, 'Categoría general', border)
            hoja.write(2, 2, 'Total', border)
            hoja.write(1, 4, 'Cantidad por talla general', border)
            hoja.write(2, 3, 'Sin talla', border)
            hoja.write(2, 4, '5', border)
            hoja.write(2, 5, '6', border)
            hoja.write(2, 6, '7', border)
            hoja.write(2, 7, '8', border)
            hoja.write(2, 8, 'A', border)
            hoja.write(2, 9, 'B', border)
            hoja.write(2, 10, 'C', border)
            hoja.write(2, 11, 'D', border)
            hoja.write(2, 12, 'XXS', border)
            hoja.write(2, 13, 'XS', border)
            hoja.write(2, 14, 'S', border)
            hoja.write(2, 15, 'M', border)
            hoja.write(2, 16, 'L', border)
            hoja.write(2, 17, 'XL', border)
            hoja.write(2, 18, '1X', border)
            hoja.write(2, 19, '2X', border)
            hoja.write(2, 20, '3X', border)
            hoja.write(2, 21, '4X', border)
            hoja.write(2, 22, '5X', border)
            x = 3
            
            productos_general = {}
            totales = {}
            totales['existencia_total'] = 0
            totales['sin_talla'] = 0
            totales['5'] = 0
            totales['6'] = 0
            totales['7'] = 0
            totales['8'] = 0
            totales['A'] = 0
            totales['B'] = 0
            totales['C'] = 0
            totales['D'] = 0
            totales['XXS'] = 0
            totales['XS'] = 0
            totales['S'] = 0
            totales['M'] = 0
            totales['L'] = 0
            totales['XL'] = 0
            totales['1X'] = 0
            totales['2X'] = 0
            totales['3X'] = 0
            totales['4X'] = 0
            totales['5X'] = 0
            
            for categoria in self.env['product.category'].search([]):
                if not categoria.parent_id:
                    if categoria.id not in productos_general:
                        productos_general[categoria.id] = {}
                        productos_general[categoria.id]['existencia_total'] = 0
                        productos_general[categoria.id]['sin_talla'] = 0
                        productos_general[categoria.id]['5'] = 0
                        productos_general[categoria.id]['6'] = 0
                        productos_general[categoria.id]['7'] = 0
                        productos_general[categoria.id]['8'] = 0
                        productos_general[categoria.id]['A'] = 0
                        productos_general[categoria.id]['B'] = 0
                        productos_general[categoria.id]['C'] = 0
                        productos_general[categoria.id]['D'] = 0
                        productos_general[categoria.id]['XXS'] = 0
                        productos_general[categoria.id]['XS'] = 0
                        productos_general[categoria.id]['S'] = 0
                        productos_general[categoria.id]['M'] = 0
                        productos_general[categoria.id]['L'] = 0
                        productos_general[categoria.id]['XL'] = 0
                        productos_general[categoria.id]['1X'] = 0
                        productos_general[categoria.id]['2X'] = 0
                        productos_general[categoria.id]['3X'] = 0
                        productos_general[categoria.id]['4X'] = 0
                        productos_general[categoria.id]['5X'] = 0
                        
                    for producto in  self.env['product.product'].with_context({'to_date': dic['fecha_hasta'].strftime("%Y-%m-%d  %H:%M:%S")}).search([('type', '=', 'product')]):
                        if producto.categ_id.name == categoria.name or producto.categ_id.parent_id.name == categoria.name or producto.categ_id.parent_id.parent_id.name == categoria.name:
                            productos_general[categoria.id]['existencia_total'] += producto.qty_available
                            if producto.product_template_variant_value_ids:
                                for attribute_line in producto.product_template_variant_value_ids:
                                    if attribute_line.name == '5':
                                        productos_general[categoria.id]['5'] += producto.qty_available
                                    elif attribute_line.name == '6':
                                        productos_general[categoria.id]['6'] += producto.qty_available
                                    elif attribute_line.name == '7':
                                        productos_general[categoria.id]['7'] += producto.qty_available
                                    elif attribute_line.name == '8':
                                        productos_general[categoria.id]['8'] += producto.qty_available
                                    elif attribute_line.name == 'A':
                                        productos_general[categoria.id]['A'] += producto.qty_available
                                    elif attribute_line.name == 'B':
                                        productos_general[categoria.id]['B'] += producto.qty_available
                                    elif attribute_line.name == 'C':
                                        productos_general[categoria.id]['C'] += producto.qty_available
                                    elif attribute_line.name == 'D':
                                        productos_general[categoria.id]['D'] += producto.qty_available
                                    elif attribute_line.name == 'XXS':
                                        productos_general[categoria.id]['XXS'] += producto.qty_available
                                    elif attribute_line.name == 'XS':
                                        productos_general[categoria.id]['XS'] += producto.qty_available
                                    elif attribute_line.name == 'S':
                                        productos_general[categoria.id]['S'] += producto.qty_available
                                    elif attribute_line.name == 'M':
                                        productos_general[categoria.id]['M'] += producto.qty_available
                                    elif attribute_line.name == 'L':
                                        productos_general[categoria.id]['L'] += producto.qty_available
                                    elif attribute_line.name == 'XL':
                                        productos_general[categoria.id]['XL'] += producto.qty_available
                                    elif attribute_line.name == '1X':
                                        productos_general[categoria.id]['1X'] += producto.qty_available
                                    elif attribute_line.name == '2X':
                                        productos_general[categoria.id]['2X'] += producto.qty_available
                                    elif attribute_line.name == '3X':
                                        productos_general[categoria.id]['3X'] += producto.qty_available
                                    elif attribute_line.name == '4X':
                                        productos_general[categoria.id]['4X'] += producto.qty_available
                                    elif attribute_line.name == '5X':
                                        productos_general[categoria.id]['5X'] += producto.qty_available
                                    else:
                                        productos_general[categoria.id]['sin_talla'] += producto.qty_available
                            else:
                                productos_general[categoria.id]['sin_talla'] += line.quantity
                                
                    totales['existencia_total'] += productos_general[categoria.id]['existencia_total']
                    totales['sin_talla'] += productos_general[categoria.id]['sin_talla']
                    totales['5'] += productos_general[categoria.id]['5']
                    totales['6'] += productos_general[categoria.id]['6']
                    totales['7'] += productos_general[categoria.id]['7']
                    totales['8'] += productos_general[categoria.id]['8']
                    totales['A'] += productos_general[categoria.id]['A']
                    totales['B'] += productos_general[categoria.id]['B']
                    totales['C'] += productos_general[categoria.id]['C']
                    totales['D'] += productos_general[categoria.id]['C']
                    totales['XXS'] += productos_general[categoria.id]['XXS']
                    totales['XS'] += productos_general[categoria.id]['XS']
                    totales['S'] += productos_general[categoria.id]['S']
                    totales['M'] += productos_general[categoria.id]['M']
                    totales['L'] += productos_general[categoria.id]['L']
                    totales['XL'] += productos_general[categoria.id]['XL']
                    totales['1X'] += productos_general[categoria.id]['1X']
                    totales['2X'] += productos_general[categoria.id]['2X']
                    totales['3X'] += productos_general[categoria.id]['3X']
                    totales['4X'] += productos_general[categoria.id]['4X']
                    totales['5X'] += productos_general[categoria.id]['5X']
                    hoja.write(x, 1, categoria.name)
                    hoja.write(x, 2, productos_general[categoria.id]['existencia_total'])
                    hoja.write(x, 3, productos_general[categoria.id]['sin_talla'])
                    hoja.write(x, 4, productos_general[categoria.id]['5'])
                    hoja.write(x, 5, productos_general[categoria.id]['6'])
                    hoja.write(x, 6, productos_general[categoria.id]['7'])
                    hoja.write(x, 7, productos_general[categoria.id]['8'])
                    hoja.write(x, 8, productos_general[categoria.id]['A'])
                    hoja.write(x, 9, productos_general[categoria.id]['B'])
                    hoja.write(x, 10, productos_general[categoria.id]['C'])
                    hoja.write(x, 11, productos_general[categoria.id]['D'])
                    hoja.write(x, 12, productos_general[categoria.id]['XXS'])
                    hoja.write(x, 13, productos_general[categoria.id]['XS'])
                    hoja.write(x, 14, productos_general[categoria.id]['S'])
                    hoja.write(x, 15, productos_general[categoria.id]['M'])
                    hoja.write(x, 16, productos_general[categoria.id]['L'])
                    hoja.write(x, 17, productos_general[categoria.id]['XL'])
                    hoja.write(x, 18, productos_general[categoria.id]['1X'])
                    hoja.write(x, 19, productos_general[categoria.id]['2X'])
                    hoja.write(x, 20, productos_general[categoria.id]['3X'])
                    hoja.write(x, 21, productos_general[categoria.id]['4X'])
                    hoja.write(x, 22, productos_general[categoria.id]['5X'])
                    x += 1
            
            hoja.write(x, 1, 'TOTALES', bold)  
            hoja.write(x, 2, totales['existencia_total'], bold)  
            hoja.write(x, 3, totales['sin_talla'], bold)  
            hoja.write(x, 4, totales['5'], bold)  
            hoja.write(x, 5, totales['6'], bold)  
            hoja.write(x, 6, totales['7'], bold)  
            hoja.write(x, 7, totales['8'], bold)  
            hoja.write(x, 8, totales['A'], bold)  
            hoja.write(x, 9, totales['B'], bold)  
            hoja.write(x, 10, totales['C'], bold)  
            hoja.write(x, 11, totales['D'], bold)  
            hoja.write(x, 12, totales['XXS'], bold)  
            hoja.write(x, 13, totales['XS'], bold)  
            hoja.write(x, 14, totales['S'], bold)  
            hoja.write(x, 15, totales['M'], bold)  
            hoja.write(x, 16, totales['L'], bold)  
            hoja.write(x, 17, totales['XL'], bold)  
            hoja.write(x, 18, totales['1X'], bold)  
            hoja.write(x, 19, totales['2X'], bold)  
            hoja.write(x, 20, totales['3X'], bold)  
            hoja.write(x, 21, totales['4X'], bold)  
            hoja.write(x, 22, totales['5X'], bold) 
                    
            libro.close()
            datos = base64.b64encode(f.getvalue())
            self.write({'archivo':datos, 'name':'reporte_inventario.xlsx'})

        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'amirah.reporte_inventario',
            'res_id': self.id,
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }