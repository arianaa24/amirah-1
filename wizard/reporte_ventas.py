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
            
            tallas_encabezado = []
            productos_general = {}
            totales = {}
            totales['total_vendidos'] = 0
            totales['sin_talla'] = 0
            
            for line in self.env['account.move.line'].search([('date','>=',dic['fecha_desde']), ('date','<=',dic['fecha_hasta']), ('parent_state','=','posted'), ('move_id.move_type','=','out_invoice')]):
                
                if line.product_id.categ_id.parent_id:
                    if line.product_id.categ_id.parent_id.parent_id:
                        categoria = line.product_id.categ_id.parent_id.parent_id
                    else:
                        categoria = line.product_id.categ_id.parent_id
                else:
                    categoria = line.product_id.categ_id
                    
                if categoria:
                    if categoria.id not in productos_general:
                        productos_general[categoria.id] = {}
                    if line.product_id.categ_id.name not in productos_general[categoria.id]:
                        productos_general[categoria.id][line.product_id.categ_id.name] = {}
                        productos_general[categoria.id][line.product_id.categ_id.name]['nombre_categoría'] = categoria.name
                        productos_general[categoria.id][line.product_id.categ_id.name]['nombre_subcategoría'] = line.product_id.categ_id.name
                        productos_general[categoria.id][line.product_id.categ_id.name]['total_vendidos'] = 0
                        productos_general[categoria.id][line.product_id.categ_id.name]['sin_talla'] = 0
                    
                    productos_general[categoria.id][line.product_id.categ_id.name]['total_vendidos'] += line.quantity
                    totales['total_vendidos'] += line.quantity
    
                    if line.product_id.product_template_variant_value_ids:
                        no_es_talla = 0
                        for attribute_line in line.product_id.product_template_variant_value_ids:
                            if 'Tallas' in attribute_line.attribute_id.name:
                                if attribute_line.name not in productos_general[categoria.id][line.product_id.categ_id.name]:
                                    productos_general[categoria.id][line.product_id.categ_id.name][attribute_line.name] = 0
                                if attribute_line.name not in totales:
                                    totales[attribute_line.name] = 0
                                if attribute_line.name not in tallas_encabezado:
                                    tallas_encabezado.append(attribute_line.name)
                                    
                                productos_general[categoria.id][line.product_id.categ_id.name][attribute_line.name] += line.quantity
                                totales[attribute_line.name] += line.quantity
                            else:
                                no_es_talla = 1
                        if no_es_talla == len(line.product_id.product_template_variant_value_ids):
                            productos_general[categoria.id][line.product_id.categ_id.name]['sin_talla'] += line.quantity
                            totales['sin_talla'] += line.quantity
                    else:
                        productos_general[categoria.id][line.product_id.categ_id.name]['sin_talla'] += line.quantity
                        totales['sin_talla'] += line.quantity
            
            y = 5
            for talla in tallas_encabezado:
                hoja.write(2, y, talla, border)
                y += 1
            
            x = 3
            for categoria in productos_general.values():
                for subcategoria in categoria.values():
                    hoja.write(x, 1, subcategoria['nombre_categoría'])
                    hoja.write(x, 2, subcategoria['nombre_subcategoría'])
                    hoja.write(x, 3, subcategoria['total_vendidos'])
                    hoja.write(x, 4, subcategoria['sin_talla'])
                    
                    y = 5
                    for talla in tallas_encabezado:
                        if talla in subcategoria:
                            hoja.write(x, y, subcategoria[talla])
                        else:
                            hoja.write(x, y, 0)
                        y += 1
                x += 1
                
            hoja.write(x, 1, 'TOTALES', bold)  
            hoja.write(x, 3, totales['total_vendidos'], bold)  
            hoja.write(x, 4, totales['sin_talla'], bold)  
            y = 5
            for talla in tallas_encabezado:
                if talla in totales:
                    hoja.write(x, y, totales[talla], bold)
                else:
                    hoja.write(x, y, 0, bold)
                y += 1
            
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