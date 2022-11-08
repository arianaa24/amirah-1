# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import base64
import io
import logging
import xlsxwriter

class WizardReporteVentas(models.TransientModel):
    _name = 'amirah.reporte_ventas'
    
    fecha_desde = fields.Date('Fecha inicio', required=True, default=fields.Datetime.now)
    fecha_hasta = fields.Date('Fecha fin', required=True, default=fields.Datetime.now)
    
    name = fields.Char('Nombre archivo')
    archivo = fields.Binary('Archivo')
    
    def print_report_excel(self):
        for w in self:
            dic = {}
            dic['fecha_desde'] = w['fecha_desde']
            dic['fecha_hasta'] = w['fecha_hasta']
            
            f = io.BytesIO()
            libro = xlsxwriter.Workbook(f) 
            hoja = libro.add_worksheet('Ventas')
            bold = libro.add_format({'bold': True})
            border = libro.add_format({'border': 1, 'bold': True})
            
            hoja.write(0, 4, 'Del ' + str(dic['fecha_desde']) + ' al ' + str(dic['fecha_hasta']), bold)
            hoja.write(2, 1, 'Categoría general', border)
            hoja.write(2, 2, 'Subcategoría', border)
            hoja.write(2, 3, 'Total', border)
            hoja.write(1, 4, 'Cantidad por talla general', border)
            hoja.write(2, 4, 'Sin talla', border)
            hoja.write(2, 5, '5', border)
            hoja.write(2, 6, '6', border)
            hoja.write(2, 7, '7', border)
            hoja.write(2, 8, '8', border)
            hoja.write(2, 9, 'A', border)
            hoja.write(2, 10, 'B', border)
            hoja.write(2, 11, 'C', border)
            hoja.write(2, 12, 'D', border)
            hoja.write(2, 13, 'XXS', border)
            hoja.write(2, 14, 'XS', border)
            hoja.write(2, 15, 'S', border)
            hoja.write(2, 16, 'M', border)
            hoja.write(2, 17, 'L', border)
            hoja.write(2, 18, 'XL', border)
            hoja.write(2, 19, '1X', border)
            hoja.write(2, 20, '2X', border)
            hoja.write(2, 21, '3X', border)
            hoja.write(2, 22, '4X', border)
            hoja.write(2, 23, '5X', border)
            x = 3
            
            productos_general = {}
            totales = {}
            totales['total_vendidos'] = 0
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
                        
                    for line in self.env['account.move.line'].search([('date','>=',dic['fecha_desde']), ('date','<=',dic['fecha_hasta']), ('parent_state','=','posted'), ('move_id.move_type','=','out_invoice')]):
                        if line.product_id.categ_id.name == categoria.name or line.product_id.categ_id.parent_id.name == categoria.name or line.product_id.categ_id.parent_id.parent_id.name == categoria.name:
                            if line.product_id.categ_id.name not in productos_general[categoria.id]:
                                productos_general[categoria.id][line.product_id.categ_id.name] = {}
                                productos_general[categoria.id][line.product_id.categ_id.name]['subcategoría'] = line.product_id.categ_id.name
                                productos_general[categoria.id][line.product_id.categ_id.name]['total_vendidos'] = 0
                                productos_general[categoria.id][line.product_id.categ_id.name]['sin_talla'] = 0
                                productos_general[categoria.id][line.product_id.categ_id.name]['5'] = 0
                                productos_general[categoria.id][line.product_id.categ_id.name]['6'] = 0
                                productos_general[categoria.id][line.product_id.categ_id.name]['7'] = 0
                                productos_general[categoria.id][line.product_id.categ_id.name]['8'] = 0
                                productos_general[categoria.id][line.product_id.categ_id.name]['A'] = 0
                                productos_general[categoria.id][line.product_id.categ_id.name]['B'] = 0
                                productos_general[categoria.id][line.product_id.categ_id.name]['C'] = 0
                                productos_general[categoria.id][line.product_id.categ_id.name]['D'] = 0
                                productos_general[categoria.id][line.product_id.categ_id.name]['XXS'] = 0
                                productos_general[categoria.id][line.product_id.categ_id.name]['XS'] = 0
                                productos_general[categoria.id][line.product_id.categ_id.name]['S'] = 0
                                productos_general[categoria.id][line.product_id.categ_id.name]['M'] = 0
                                productos_general[categoria.id][line.product_id.categ_id.name]['L'] = 0
                                productos_general[categoria.id][line.product_id.categ_id.name]['XL'] = 0
                                productos_general[categoria.id][line.product_id.categ_id.name]['1X'] = 0
                                productos_general[categoria.id][line.product_id.categ_id.name]['2X'] = 0
                                productos_general[categoria.id][line.product_id.categ_id.name]['3X'] = 0
                                productos_general[categoria.id][line.product_id.categ_id.name]['4X'] = 0
                                productos_general[categoria.id][line.product_id.categ_id.name]['5X'] = 0
                           
                            productos_general[categoria.id][line.product_id.categ_id.name]['total_vendidos'] += line.quantity
                            if line.product_id.product_template_variant_value_ids:
                                for attribute_line in line.product_id.product_template_variant_value_ids:
                                    if attribute_line.name == '5':
                                        productos_general[categoria.id][line.product_id.categ_id.name]['5'] += line.quantity
                                    elif attribute_line.name == '6':
                                        productos_general[categoria.id][line.product_id.categ_id.name]['6'] += line.quantity
                                    elif attribute_line.name == '7':
                                        productos_general[categoria.id][line.product_id.categ_id.name]['7'] += line.quantity
                                    elif attribute_line.name == '8':
                                        productos_general[categoria.id][line.product_id.categ_id.name]['8'] += line.quantity
                                    elif attribute_line.name == 'A':
                                        productos_general[categoria.id][line.product_id.categ_id.name]['A'] += line.quantity
                                    elif attribute_line.name == 'B':
                                        productos_general[categoria.id][line.product_id.categ_id.name]['B'] += line.quantity
                                    elif attribute_line.name == 'C':
                                        productos_general[categoria.id][line.product_id.categ_id.name]['C'] += line.quantity
                                    elif attribute_line.name == 'D':
                                        productos_general[categoria.id][line.product_id.categ_id.name]['D'] += line.quantity
                                    elif attribute_line.name == 'XXS':
                                        productos_general[categoria.id][line.product_id.categ_id.name]['XXS'] += line.quantity
                                    elif attribute_line.name == 'XS':
                                        productos_general[categoria.id][line.product_id.categ_id.name]['XS'] += line.quantity
                                    elif attribute_line.name == 'S':
                                        productos_general[categoria.id][line.product_id.categ_id.name]['S'] += line.quantity
                                    elif attribute_line.name == 'M':
                                        productos_general[categoria.id][line.product_id.categ_id.name]['M'] += line.quantity
                                    elif attribute_line.name == 'L':
                                        productos_general[categoria.id][line.product_id.categ_id.name]['L'] += line.quantity
                                    elif attribute_line.name == 'XL':
                                        productos_general[categoria.id][line.product_id.categ_id.name]['XL'] += line.quantity
                                    elif attribute_line.name == '1XL':
                                        productos_general[categoria.id][line.product_id.categ_id.name]['1X'] += line.quantity
                                    elif attribute_line.name == '2XL':
                                        productos_general[categoria.id][line.product_id.categ_id.name]['2X'] += line.quantity
                                    elif attribute_line.name == '3XL':
                                        productos_general[categoria.id][line.product_id.categ_id.name]['3X'] += line.quantity
                                    elif attribute_line.name == '4XL':
                                        productos_general[categoria.id][line.product_id.categ_id.name]['4X'] += line.quantity
                                    elif attribute_line.name == '5XL':
                                        productos_general[categoria.id][line.product_id.categ_id.name]['5X'] += line.quantity
                                    else:
                                        productos_general[categoria.id][line.product_id.categ_id.name]['sin_talla'] += line.quantity
                            else:
                                productos_general[categoria.id][line.product_id.categ_id.name]['sin_talla'] += line.quantity
                   
                    for subcategoría in productos_general[categoria.id]:
                        totales['total_vendidos'] += productos_general[categoria.id][subcategoría]['total_vendidos']
                        totales['sin_talla'] += productos_general[categoria.id][subcategoría]['sin_talla']
                        totales['5'] += productos_general[categoria.id][subcategoría]['5']
                        totales['6'] += productos_general[categoria.id][subcategoría]['6']
                        totales['7'] += productos_general[categoria.id][subcategoría]['7']
                        totales['8'] += productos_general[categoria.id][subcategoría]['8']
                        totales['A'] += productos_general[categoria.id][subcategoría]['A']
                        totales['B'] += productos_general[categoria.id][subcategoría]['B']
                        totales['C'] += productos_general[categoria.id][subcategoría]['C']
                        totales['D'] += productos_general[categoria.id][subcategoría]['D']
                        totales['XXS'] += productos_general[categoria.id][subcategoría]['XXS']
                        totales['XS'] += productos_general[categoria.id][subcategoría]['XS']
                        totales['S'] += productos_general[categoria.id][subcategoría]['S']
                        totales['M'] += productos_general[categoria.id][subcategoría]['M']
                        totales['L'] += productos_general[categoria.id][subcategoría]['L']
                        totales['XL'] += productos_general[categoria.id][subcategoría]['XL']
                        totales['1X'] += productos_general[categoria.id][subcategoría]['1X']
                        totales['2X'] += productos_general[categoria.id][subcategoría]['2X']
                        totales['3X'] += productos_general[categoria.id][subcategoría]['3X']
                        totales['4X'] += productos_general[categoria.id][subcategoría]['4X']
                        totales['5X'] += productos_general[categoria.id][subcategoría]['5X']
                        hoja.write(x, 1, categoria.name)
                        hoja.write(x, 2, productos_general[categoria.id][subcategoría]['subcategoría'])
                        hoja.write(x, 3, productos_general[categoria.id][subcategoría]['total_vendidos'])
                        hoja.write(x, 4, productos_general[categoria.id][subcategoría]['sin_talla'])
                        hoja.write(x, 5, productos_general[categoria.id][subcategoría]['5'])
                        hoja.write(x, 6, productos_general[categoria.id][subcategoría]['6'])
                        hoja.write(x, 7, productos_general[categoria.id][subcategoría]['7'])
                        hoja.write(x, 8, productos_general[categoria.id][subcategoría]['8'])
                        hoja.write(x, 9, productos_general[categoria.id][subcategoría]['A'])
                        hoja.write(x, 10, productos_general[categoria.id][subcategoría]['B'])
                        hoja.write(x, 11, productos_general[categoria.id][subcategoría]['C'])
                        hoja.write(x, 12, productos_general[categoria.id][subcategoría]['D'])
                        hoja.write(x, 13, productos_general[categoria.id][subcategoría]['XXS'])
                        hoja.write(x, 14, productos_general[categoria.id][subcategoría]['XS'])
                        hoja.write(x, 15, productos_general[categoria.id][subcategoría]['S'])
                        hoja.write(x, 16, productos_general[categoria.id][subcategoría]['M'])
                        hoja.write(x, 17, productos_general[categoria.id][subcategoría]['L'])
                        hoja.write(x, 18, productos_general[categoria.id][subcategoría]['XL'])
                        hoja.write(x, 19, productos_general[categoria.id][subcategoría]['1X'])
                        hoja.write(x, 20, productos_general[categoria.id][subcategoría]['2X'])
                        hoja.write(x, 21, productos_general[categoria.id][subcategoría]['3X'])
                        hoja.write(x, 22, productos_general[categoria.id][subcategoría]['4X'])
                        hoja.write(x, 23, productos_general[categoria.id][subcategoría]['5X'])
                        x += 1
                        
            hoja.write(x, 1, 'TOTALES', bold)  
            hoja.write(x, 3, totales['total_vendidos'], bold)  
            hoja.write(x, 4, totales['sin_talla'], bold)  
            hoja.write(x, 5, totales['5'], bold)  
            hoja.write(x, 6, totales['6'], bold)  
            hoja.write(x, 7, totales['7'], bold)  
            hoja.write(x, 8, totales['8'], bold)  
            hoja.write(x, 9, totales['A'], bold)  
            hoja.write(x, 10, totales['B'], bold)  
            hoja.write(x, 11, totales['C'], bold)  
            hoja.write(x, 12, totales['D'], bold)  
            hoja.write(x, 13, totales['XXS'], bold)  
            hoja.write(x, 14, totales['XS'], bold)  
            hoja.write(x, 15, totales['S'], bold)  
            hoja.write(x, 16, totales['M'], bold)  
            hoja.write(x, 17, totales['L'], bold)  
            hoja.write(x, 18, totales['XL'], bold)  
            hoja.write(x, 19, totales['1X'], bold)  
            hoja.write(x, 20, totales['2X'], bold)  
            hoja.write(x, 21, totales['3X'], bold)  
            hoja.write(x, 22, totales['4X'], bold)  
            hoja.write(x, 23, totales['5X'], bold) 
                    
            libro.close()
            datos = base64.b64encode(f.getvalue())
            self.write({'archivo':datos, 'name':'reporte_ventas.xlsx'})

        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'amirah.reporte_ventas',
            'res_id': self.id,
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }