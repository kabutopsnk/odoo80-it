# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011 OpenERP SA (<http://openerp.com>).
#    Application developed by: Carlos Andrés Ordóñez P.
#    Country: Ecuador
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv

from openerp.modules.module import get_module_resource
from xlrd import open_workbook
from xlutils.copy import copy


class sri2016_107_general(osv.osv):
    _name = 'sri2016.107.general'
    _description = u'SRI formulario 107 + RDEP General (2016)'
    
    _columns = {
                #'name': fields.char(u'Descripcion', size=100, required=True),
                'name': fields.many2one('res.company', u'Compañía', required=True),
                'date_start': fields.date(u'Desde', required=True),
                'date_end': fields.date(u'Hasta', required=True),
                'line_ids': fields.one2many('sri2016.107.individual', 'head_id', u'Detalle'),
                'archivo_rdep': fields.binary(u'Archivo RDEP', help='RDEP en formato XML', readonly=True),
                'name_rdep': fields.char(u'Archivo RDEP', size=100, required=True, readonly=True),
                'state': fields.selection([('draft',u'Borrador'),('done',u'Aprobado'),('cancel',u'Cancelado')],u'Estado'),
                }
    
    _defaults = {
                 'state': 'draft',
                 }
    
    def unlink(self, cr, uid, ids, *args, **kwargs):
        for this in self.browse(cr, uid, ids):
            if this.state != 'draft':
                raise osv.except_osv(u'Operación no permitida !', u'No puede eliminar, solo puede realizar esta operación en estado Borrador')
            for linea in this.line_ids:
                if linea.state!='draft':
                    raise osv.except_osv(u'Operación no permitida !', u'No puede eliminar, solo puede realizar esta operación si todas las líneas se encuentran en estado borrador')
        return super(sri2016_107_general, self).unlink(cr, uid, ids, *args, **kwargs)
    
    
sri2016_107_general()


class sri2016_107_individual(osv.osv):
    _name = "sri2016.107.individual"
    
    _columns = {
                'name': fields.char(u'Descripción', size=50, required=False, readonly=True),
                'codigo': fields.char(u'Código', size=50, required=False, readonly=True),
                #'date_start': fields.char(u'Desde', size=50, required=True),
                #'date_end': fields.char(u'Hasta', size=50, required=True),
                'head_id': fields.many2one('sri2016.107.general', u'Formulario Empresa', ondelete='cascade'),
                #'employee_id': fields.many2one('hr.employee', 'Empleado'),
                'field_102': fields.char(u'102 Ejercicio Fiscal', size=10, required=True),
                #'field_102': fields.many2one('hr.contract.wage.type.period', 'Ejercicio Fiscal - 102'),
                'field_103': fields.date(u'103 Fecha', required=True),
                'field_105': fields.char(u'105 Empleador - RUC', size=13),
                'field_106': fields.char(u'106 Empleador - Nombre', size=50),
                'field_201': fields.char(u'201 Empleado - Cédula o Pasaporte', size=15),
                #'field_202': fields.char('Empleado - Nombre - 202', size=50),
                'field_202': fields.many2one('hr.employee', u'202 Empleado - Nombre', required=True),
                'field_301': fields.float(u'301 Sueldos y salarios'),
                'field_303': fields.float(u'303 Sobresueldos, comisiones, bonos y otras remuneraciones gravadas'),
                'field_305': fields.float(u'305 Participación de utilidades'),
                'field_307': fields.float(u'307 Ingresos gravados generados con otros empleadores'),
                #'field_309': fields.float('Fondos de reserva - 309'),
                'field_311': fields.float(u'311 Décimo Tercero'),
                'field_313': fields.float(u'313 Décimo Cuarto'),
                'field_315': fields.float(u'315 Fondo de Reserva'),
                'field_317': fields.float(u'317 Otros ingresos en relacion de dependencia que no constituyen renta gravada'),
                'field_349': fields.float(u'349 Ingresos gravados con este empleador'),
                'field_351': fields.float(u'351 Aporte Personal IESS con este empleador'),
                'field_353': fields.float(u'353 Aporte Personal IESS con otros Empleadores'),
                'field_361': fields.float(u'361 Deducción gastos personales - Vivienda'),
                'field_363': fields.float(u'363 Deducción gastos personales - Salud'),
                'field_365': fields.float(u'365 Deducción gastos personales - Educación'),
                'field_367': fields.float(u'367 Deducción gastos personales - Alimentación'),
                'field_369': fields.float(u'369 Deducción gastos personales - Vestimenta'),
                'field_371': fields.float(u'371 Exoneración por discapacidad'),
                'field_373': fields.float(u'373 Exoneración por tercera edad'),
                'field_381': fields.float(u'381 Impuesto a la renta asumido por este empleador'),
                'field_399': fields.float(u'399 Base imponible Gravada'),
                'field_401': fields.float(u'401 Impuesto a la renta causado'),
                'field_403': fields.float(u'403 Impuesto a la renta retenido y asumido por empleadores durante el periodo declarado'),
                'field_405': fields.float(u'405 Impuesto a la renta asumido por este empleador'),
                'field_407': fields.float(u'407 Impuesto a la renta retenido al trabajador por este empleador'),
                'detalle': fields.text(u'Detalle'),
                'archivo': fields.binary(u'Archivo', readonly=True),
                #'archivo_fname': fields.char('Nombre del Archivo', readonly=True, size=100),
                'state': fields.selection([('draft',u'Borrador'),('done',u'Aprobado'),('cancel',u'Cancelado')],u'Estado'),
                }
    
    _defaults = {
                 'state': 'draft',
                 }
    
    def unlink(self, cr, uid, ids, *args, **kwargs):
        for this in self.browse(cr, uid, ids):
            if this.state != 'draft':
                raise osv.except_osv(u'Operación no permitida !', u'No puede eliminar, solo puede realizar esta operación en estado Borrador')
        return super(sri2016_107_individual, self).unlink(cr, uid, ids, *args, **kwargs)
    
    def calcular_exportar(self, cr, uid, ids, context=None):
        self.calcular_formulario(cr, uid, ids, context)
        #directorio = os.system("mkdir formularios107")
        #return self.crear_xls107(cr, uid, ids, context=context)

    def calcular_formulario(self, cr, uid, ids, context=None):
        tabla_pool = self.pool.get('hr.sri.taxable')
        line_pool = self.pool.get('hr.sri.taxable.line')
        #obj_provision = self.pool.get('hr.provision.line')
        #obj_dec_tercer = self.pool.get('hr.dec.tercer.line')
        #obj_dec_cuarto = self.pool.get('hr.dec.cuarto.line')
        #obj_utilidades = self.pool.get('hr.utilities.line')
        obj_projection = self.pool.get('hr.employee.projection')
        obj_payslip = self.pool.get('hr.payslip')
        obj_renta = self.pool.get('hr.employee.profit')
        
        #usuario = self.pool.get('res.users').browse(cr, uid, uid, context)
        
        for formulario in self.browse(cr, uid, ids, context=context):
            if formulario.head_id:
                fecha_inicio = formulario.head_id.date_start
                fecha_fin = formulario.head_id.date_end
            else:
                fecha_inicio = formulario.field_102 + "-01-01"
                #fecha_fin = formulario.field_102 + "-12-31"
                fecha_fin = formulario.field_103
            datos = {#'field_103': time.strftime('%Y-%m-%d'),
                     'field_105': formulario.field_202.contract_id.company_id.ruc,
                     'field_106': formulario.field_202.contract_id.company_id.name,
                     'field_201': formulario.field_202.name,
                     'field_301': 0.0,
                     'field_303': 0.0,
                     'field_305': 0.0,
                     'field_307': 0.0,
                     'field_311': 0.0,
                     'field_313': 0.0,
                     'field_315': 0.0,
                     'field_317': 0.0,
                     'field_351': 0.0,
                     'field_353': 0.0,
                     'field_361': 0.0,
                     'field_363': 0.0,
                     'field_365': 0.0,
                     'field_367': 0.0,
                     'field_369': 0.0,
                     'field_371': 0.0,
                     'field_373': 0.0,
                     'field_381': 0.0,
                     'field_399': 0.0,
                     'field_401': 0.0,
                     'field_403': 0.0,
                     'field_405': 0.0,
                     'field_407': 0.0,
                     'field_349': 0.0,
                     'detalle': '',
                     }
            #print 1
            #MIGRAR RUBROS ANTERIORES
            try:
                obj_extras = self.pool.get('sri2016.107.rubro')
                ids_extras = obj_extras.search(cr, uid, [('date','>=',fecha_inicio),
                                                         ('date','<=',fecha_fin),
                                                         ('employee_id','=',formulario.field_202.id)])
                for extra in obj_extras.browse(cr, uid, ids_extras):
                    datos[extra.name] = datos[extra.name] + extra.valor
            except:
                pass
            #print 2
            #period_ids = obj_period.search(cr, uid, [('period_id','=',formulario.field_102.id)])
            payslip_ids = obj_payslip.search(cr, uid, [('employee_id','=',formulario.field_202.id),
                                                       ('date_from','>=',fecha_inicio),
                                                       ('date_to','<=',fecha_fin),
                                                       ('state','=','done'),
                                                       #('payroll_type','=','monthly'),
                                                       ], context=context)
            for payslip in obj_payslip.browse(cr, uid, payslip_ids, context=context):
                for linea in payslip.line_ids:
                    if linea.salary_rule_id.sri2016_107:
                        datos[linea.salary_rule_id.sri2016_107] += linea.total
            #proyecciones
            for proyeccion_anual in formulario.field_202.projection_lines:
                #import pdb
                #pdb.set_trace()
                #if proyeccion_anual.date_start>=fecha_inicio and proyeccion_anual.date_stop<=fecha_fin:
                if proyeccion_anual.date_start<=formulario.field_103 and proyeccion_anual.date_stop>=formulario.field_103:
                    datos['field_361']=0.0
                    datos['field_363']=0.0
                    datos['field_365']=0.0
                    datos['field_367']=0.0
                    datos['field_369']=0.0
                    datos['field_371']=0.0
                    datos['field_373']=0.0
                    for linea in proyeccion_anual.line_ids:
                        if linea.name.name.upper()=="VIVIENDA":
                            datos['field_361'] = datos['field_361'] + linea.value
                            datos['detalle'] = datos['detalle'] + '\n' + proyeccion_anual.name + ' - 361 - Vivienda: ' + str(linea.value)
                        if linea.name.name.upper()=="SALUD":
                            datos['field_363'] = datos['field_363'] + linea.value
                            datos['detalle'] = datos['detalle'] + '\n' + proyeccion_anual.name + ' - 363 - Salud: ' + str(linea.value)
                        if linea.name.name.upper()=="EDUCACION":
                            datos['field_365'] = datos['field_365'] + linea.value
                            datos['detalle'] = datos['detalle'] + '\n' + proyeccion_anual.name + ' - 365 - Educacion: ' + str(linea.value)
                        if linea.name.name.upper()=="ALIMENTACION":
                            datos['field_367'] = datos['field_367'] + linea.value
                            datos['detalle'] = datos['detalle'] + '\n' + proyeccion_anual.name + ' - 367 - Alimentacion: ' + str(linea.value)
                        if linea.name.name.upper()=="VESTIMENTA":
                            datos['field_369'] = datos['field_369'] + linea.value
                            datos['detalle'] = datos['detalle'] + '\n' + proyeccion_anual.name + ' - 369 - Vestimenta: ' + str(linea.value)
                        if linea.name.name.upper()=="DISCAPACIDAD":
                            datos['field_371'] = datos['field_371'] + linea.value
                            datos['detalle'] = datos['detalle'] + '\n' + proyeccion_anual.name + ' - 371 - Discapacidad: ' + str(linea.value)
                        if linea.name.name.upper()=="TERCERA EDAD":
                            datos['field_373'] = datos['field_373'] + linea.value
                            datos['detalle'] = datos['detalle'] + '\n' + proyeccion_anual.name + ' - 373 - Tercera Edad: ' + str(linea.value)
            #Valor retenido
            for renta_anual in formulario.field_202.profit_lines:
              if renta_anual.date_start>=fecha_inicio and renta_anual.date_stop<=fecha_fin:
                for linea in renta_anual.line_ids:
                  datos['field_403'] = datos['field_403'] + linea.otros_empleadores_retenido
                  datos['field_307'] = datos['field_307'] + linea.otros_empleadores
                  datos['field_353'] = datos['field_353'] + linea.otros_empleadores_iess
                  #if linea.name=='utilidades':
                  #  datos['field_305'] = datos['field_305'] + linea.no_proyectar_no_aportable
                  #if linea.name=='decimotercero':
                  #  datos['field_311'] = datos['field_311'] + linea.no_proyectar_no_aportable
                  #if linea.name=='decimocuarto':
                  #  datos['field_313'] = datos['field_313'] + linea.no_proyectar_no_aportable
                  if linea.name=='otro':
                    datos['field_303'] = datos['field_303'] + (linea.proyectar_aportable or 0.0)
                    datos['field_303'] = datos['field_303'] + (linea.proyectar_no_aportable or 0.0)
                    datos['field_303'] = datos['field_303'] + (linea.no_proyectar_aportable or 0.0)
                    datos['field_303'] = datos['field_303'] + (linea.no_proyectar_no_aportable or 0.0)
            datos['field_399'] = datos['field_301'] + datos['field_303'] + datos['field_305'] + datos['field_307'] - datos['field_351'] - datos['field_353'] - datos['field_361'] - datos['field_363'] - datos['field_365'] - datos['field_367'] - datos['field_369'] - datos['field_371'] - datos['field_373'] + datos['field_381']
            
            #calcular meses de trabajo
            #date_start = parser.parse(formulario.field_202.contract_id.date_start)
            #date_end_form = parser.parse(formulario.field_103)
            #dias_contrato = abs(date_end_form - date_start).days
            #meses = (dias_contrato//30.416) + formulario.field_202.contract_id.meses_ant
            #meses = (dias_contrato//30.416)
            #if meses>=12:
            #    datos['field_353'] = 12
            #else:
            #    datos['field_353'] = int(meses)
            #301+303+305+381
            datos['field_349'] = datos['field_301'] + datos['field_303'] + datos['field_305'] #+ datos['field_381']
            #impuesto a la renta
            base = datos['field_399']
            tabla_ids=tabla_pool.search(cr, uid, [('date_start','<=',formulario.field_103),('date_stop','>=',formulario.field_103),])
            #import pdb
            #pdb.set_trace()
            if tabla_ids:
                for tabla in tabla_ids:
                    linea_ids=line_pool.search(cr, uid,[('taxable_id','=',tabla),
                                                        ('basic_fraction','<=',datos['field_399']),('excess_to','>=',datos['field_399'])])
                    for linea_ in linea_ids:
                        linea=line_pool.browse(cr, uid, linea_)
                        excedente=base-linea.basic_fraction
                        imp_sobre_excedente=excedente*linea.excess_fraction_percent/100.0
                        imp_frac_basica=linea.basic_fraction_tax
                        imp_renta_anual=round(imp_sobre_excedente,2)+imp_frac_basica
                        datos['field_401'] = imp_renta_anual
            self.write(cr, uid, ids, datos)
            
    def exportar_formulario(self, cr, uid, ids, context=None):
        #archivo del formulario 107
        xls_path = get_module_resource('l10n_ec_sri107_2016','xls','Formulario 107.xls')
        #image_path = addons.get_module_resource('l10n_ec_sri107_2016','xls','sri2016_logo.bmp')
        rb = open_workbook(xls_path,formatting_info=True)
        for formulario in self.browse(cr, uid, ids):
                    #escritura de datos en el formulario de excel
                    wb = copy(rb)
                    ws = wb.get_sheet(0)
                    
                    #campo numero
                    ws.write(0,26,"   No.   " + str(formulario.codigo or '' ))
                    #ws.insert_bitmap(image_path, 0, 2)
                    #campo 102
                    anio = str(formulario.field_102)
                    ws.write(3,14,anio[:1])
                    ws.write(3,15,anio[1:2])
                    ws.write(3,16,anio[2:3])
                    ws.write(3,17,anio[3:4])
                    #campo 103
                    fecha = str(formulario.field_103)
                    ws.write(4,25,fecha[:1])
                    ws.write(4,26,fecha[1:2])
                    ws.write(4,27,fecha[2:3])
                    ws.write(4,28,fecha[3:4])
                    ws.write(4,29,fecha[5:6])
                    ws.write(4,31,fecha[6:7])
                    ws.write(4,33,fecha[8:9])
                    ws.write(4,34,fecha[9:10])
                    #campo 106
                    ws.write(7,15,formulario.field_106)
                    #campo 105
                    if formulario.field_105:
                        ws.write(7,1,formulario.field_105[:1])
                        ws.write(7,2,formulario.field_105[1:2])
                        ws.write(7,3,formulario.field_105[2:3])
                        ws.write(7,4,formulario.field_105[3:4])
                        ws.write(7,5,formulario.field_105[4:5])
                        ws.write(7,6,formulario.field_105[5:6])
                        ws.write(7,7,formulario.field_105[6:7])
                        ws.write(7,8,formulario.field_105[7:8])
                        ws.write(7,9,formulario.field_105[8:9])
                        ws.write(7,10,formulario.field_105[9:10])
                    #campo 201
                    ws.write(10,1,formulario.field_202.name)
                    #campo 202
                    ws.write(10,15,formulario.field_202.name_related)
                    #campos liquidacion de impuestos
                    ws.write(13,21,str("%0.2f" % abs(formulario.field_301)))
                    ws.write(14,21,str("%0.2f" % abs(formulario.field_303)))
                    ws.write(15,21,str("%0.2f" % abs(formulario.field_305)))
                    ws.write(16,21,str("%0.2f" % abs(formulario.field_307)))
                    ws.write(17,21,str("%0.2f" % abs(formulario.field_311)))
                    ws.write(18,21,str("%0.2f" % abs(formulario.field_313)))
                    ws.write(19,21,str("%0.2f" % abs(formulario.field_315)))
                    ws.write(20,21,str("%0.2f" % abs(formulario.field_317)))
                    ws.write(21,21,str("%0.2f" % abs(formulario.field_351)))
                    ws.write(22,21,str("%0.2f" % abs(formulario.field_353)))
                    ws.write(23,21,str("%0.2f" % abs(formulario.field_361)))
                    ws.write(24,21,str("%0.2f" % abs(formulario.field_363)))
                    ws.write(25,21,str("%0.2f" % abs(formulario.field_365)))
                    ws.write(26,21,str("%0.2f" % abs(formulario.field_367)))
                    ws.write(27,21,str("%0.2f" % abs(formulario.field_369)))
                    ws.write(28,21,str("%0.2f" % abs(formulario.field_371)))
                    ws.write(29,21,str("%0.2f" % abs(formulario.field_373)))
                    ws.write(30,21,str("%0.2f" % abs(formulario.field_381)))
                    ws.write(31,21,str("%0.2f" % abs(formulario.field_399)))
                    ws.write(32,21,str("%0.2f" % abs(formulario.field_401)))
                    ws.write(33,21,str("%0.2f" % abs(formulario.field_403)))
                    ws.write(34,21,str("%0.2f" % abs(formulario.field_405)))
                    ws.write(35,21,str("%0.2f" % abs(formulario.field_407)))
                    ws.write(36,21,str("%0.2f" % abs(formulario.field_349)))
                    
                    #almacenamiento de datos del formulario en excel
                    
                    nombre = "sri107/" + str(formulario.field_102) + " - " + formulario.field_202.name_related + ".xls"
                    wb.save(nombre)
                    out = open(nombre,"rb").read().encode("base64")
                    self.write(cr, uid, formulario.id, {'archivo':out, 'name':str(formulario.field_102) + " - " + formulario.field_202.name_related + ".xls"})
        return True
    
sri2016_107_individual()

class sri2016_107_rubro(osv.osv):
    _name = 'sri2016.107.rubro'

    _FIELDS_107 = [('field_301',u'301 SUELDOS Y SALARIOS'),
                   ('field_303',u'303 SOBRESUELDOS, COMISIONES, BONOS Y OTROS INGRESOS'),
                   ('field_305',u'305 PARTICIPACIÓN UTILIDADES'),
                   ('field_307',u'307 INGRESOS GRAVADOS GENERADOS CON OTROS EMPLEADORES'),
                   ('field_311',u'311 DÉCIMO TERCER SUELDO'),
                   ('field_313',u'313 DÉCIMO CUARTO SUELDO'),
                   ('field_315',u'315 FONDO DE RESERVA'),
                   ('field_317',u'317 OTROS INGRESOS EN RELACIÓN DE DEPENDENCIA QUE NO CONSTITUYEN RENTA GRAVADA'),
                   ('field_351',u'351 APORTE PERSONAL IESS CON ESTE EMPLEADOR'),
                   ('field_353',u'353 APORTE PERSONAL IESS CON OTROS EMPLEADORES'),
                   ('field_361',u'361 DEDUCCIÓN GASTOS PERSONALES - VIVIENDA'),
                   ('field_363',u'363 DEDUCCIÓN GASTOS PERSONALES - SALUD'),
                   ('field_365',u'365 DEDUCCIÓN GASTOS PERSONALES - EDUCACIÓN'),
                   ('field_367',u'367 DEDUCCIÓN GASTOS PERSONALES - ALIMENTACIÓN'),
                   ('field_369',u'369 DEDUCCIÓN GASTOS PERSONALES - VESTIMENTA'),
                   ('field_371',u'371 EXONERACIÓN POR DISCAPACIDAD'),
                   ('field_373',u'373 EXONERACIÓN POR TERCERA EDAD'),
                   ('field_381',u'381 IMPUESTO A LA RENTA ASUMIDO POR ESTE EMPLEADOR'),
                   ('field_403',u'403 VALOR DEL IMPUESTO RETENIDO Y ASUMIDO POR OTROS EMPLEADORES DURANTE EL PERÍODO DECLARADO'),
                   ('field_405',u'405 VALOR DEL IMPUESTO ASUMIDO POR ESTE EMPLEADOR'),
                   ('field_407',u'407 VALOR DEL IMPUESTO RETENIDO AL TRABAJADOR POR ESTE EMPLEADOR')]

    _columns = {
        'descripcion':fields.char(u'Descripción', size=64),
        'valor':fields.float(u'Valor', required=True),
        'name':fields.selection(_FIELDS_107, u'Casillero', required=True),
        'employee_id':fields.many2one('hr.employee', u'Empleado', required=True, ondelete='cascade'),
        'date':fields.date(u'Fecha', required=True),
        }

    _order = 'date desc, name asc'
    
sri2016_107_rubro()

class hrEmployeeSri2016_107(osv.osv):
    _inherit = 'hr.employee'
    _columns = {
        'rubros_ids': fields.one2many('sri2016.107.rubro','employee_id', u'Rubros adicionales SRI 107 (2016)'),
        }
    
hrEmployeeSri2016_107()

class sri2016_salary_rule(osv.osv):
    _inherit = 'hr.salary.rule'
    
    _FIELDS_107 = [('field_301',u'301 SUELDOS Y SALARIOS'),
                   ('field_303',u'303 SOBRESUELDOS, COMISIONES, BONOS Y OTROS INGRESOS'),
                   ('field_305',u'305 PARTICIPACIÓN UTILIDADES'),
                   ('field_307',u'307 INGRESOS GRAVADOS GENERADOS CON OTROS EMPLEADORES'),
                   ('field_311',u'311 DÉCIMO TERCER SUELDO'),
                   ('field_313',u'313 DÉCIMO CUARTO SUELDO'),
                   ('field_315',u'315 FONDO DE RESERVA'),
                   ('field_317',u'317 OTROS INGRESOS EN RELACIÓN DE DEPENDENCIA QUE NO CONSTITUYEN RENTA GRAVADA'),
                   ('field_351',u'351 APORTE PERSONAL IESS CON ESTE EMPLEADOR'),
                   ('field_353',u'353 APORTE PERSONAL IESS CON OTROS EMPLEADORES'),
                   ('field_361',u'361 DEDUCCIÓN GASTOS PERSONALES - VIVIENDA'),
                   ('field_363',u'363 DEDUCCIÓN GASTOS PERSONALES - SALUD'),
                   ('field_365',u'365 DEDUCCIÓN GASTOS PERSONALES - EDUCACIÓN'),
                   ('field_367',u'367 DEDUCCIÓN GASTOS PERSONALES - ALIMENTACIÓN'),
                   ('field_369',u'369 DEDUCCIÓN GASTOS PERSONALES - VESTIMENTA'),
                   ('field_371',u'371 EXONERACIÓN POR DISCAPACIDAD'),
                   ('field_373',u'373 EXONERACIÓN POR TERCERA EDAD'),
                   ('field_381',u'381 IMPUESTO A LA RENTA ASUMIDO POR ESTE EMPLEADOR'),
                   ('field_403',u'403 VALOR DEL IMPUESTO RETENIDO Y ASUMIDO POR OTROS EMPLEADORES DURANTE EL PERÍODO DECLARADO'),
                   ('field_405',u'405 VALOR DEL IMPUESTO ASUMIDO POR ESTE EMPLEADOR'),
                   ('field_407',u'407 VALOR DEL IMPUESTO RETENIDO AL TRABAJADOR POR ESTE EMPLEADOR')]
    
    _columns = {
        'sri2016_107': fields.selection(_FIELDS_107, u' [2016] Formulario 107'),
        }
    
hrEmployeeSri2016_107()

