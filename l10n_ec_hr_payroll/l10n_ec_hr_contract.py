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
import datetime
import unicodedata
from time import strftime

class hr_contract_log(osv.osv):
    _name = "hr.contract.log"
    _description = "Historial de contrato"
    
    _columns = {
        'name': fields.selection([('wage','Salario'),
                                  ('department_id','Departamento'),
                                  ('job_id','Puesto de Trabajo'),
                                  ('centro_costo_id','Centro de Costo'),
                                  ('city_id','Ciudad'),
                                  ('coach_id','Jefe'),
                                  ('company_id','Empresa')], u'Campo Actualizado', required=True),
        'date': fields.date(u'Fecha de actualización', required=True),
        'previous_value': fields.char(u'Valor anterior', required=True),
        'new_value': fields.char(u'Valor nuevo', required=True),
        'contract_id': fields.many2one('hr.contract', u'Contrato', ondelete='cascade'),
    }
    
    _order = "date desc"
    
hr_contract_log()

class l10n_ec_hr_contract(osv.osv):
    _inherit = "hr.contract"
    _description = "Contrato de empleado"
    
    _columns = {
        'company_id': fields.many2one('res.company', u'Empresa'),
        'log_ids': fields.one2many('hr.contract.log', 'contract_id', u'Historial'),
        'fondo_reserva': fields.boolean(u'Fondo reserva en rol', help="Marcar la casilla si el empleado recibirá los fondos de reserva en el rol (usar 'fondo_reserva' en las formulas)"),
        'extension_iess': fields.boolean(u'Extensión de cobertura IESS', help="Marcar la casilla si el empleado ha solicitado la extensión de cobertura familiar para el IESS (usar 'extension_iess' en las formulas)"),
        'bono_alimentacion': fields.float(u'Bono de alimentación', help="Este valor puede ser utilizado como referencia de bono de alimentación en el rol de pagos (usar 'bono_alimentacion' en las formulas)"),
        'bono_transporte': fields.float(u'Bono de transporte', help="Este valor puede ser utilizado como referencia de bono de transporte en el rol de pagos (usar 'bono_transporte' en las formulas)"),
        'bono_fijo': fields.float(u'Bono fijo'),
        'bono_eficiencia': fields.float(u'Bono eficiencia'),
        'department_id': fields.many2one('hr.department', u"Departmento"),
        'city_id': fields.many2one('res.country.state.city', u"Ciudad"),
        'previous_contract': fields.boolean(u'Posee contrato anterior?', help=u"Marcar la casilla si existen contratos anteriores del empleado en la empresa"),
        'previous_contract_id': fields.many2one('hr.contract', u'Contrato anterior', help=u"Seleccione el último contrato del empleado en la empresa"),
        'previous_days': fields.float(u'Dias adicionales en la empresa', help=u"Este valor puede ser utilizado como los días que el empleado ya ha laborado antes del presente contrato en la empresa (usar 'previous_days' en las formulas)"),
        #'contract_holidays': fields.boolean(u'Posee contrato anterior para vacaciones?', help=u"Marcar la casilla si el presente contrato cuenta como la continuación de un contrato anterior y aplica para el cálculo de vacaciones"),
        #'contract_holidays_id': fields.many2one('hr.contract', u'Contrato anterior para vacaciones'),
        'date_holidays': fields.date(u'Fecha para Vacaciones'),
        'biweekly_percent': fields.float(u'Porcentaje de quincena', required=True),
        'seguro_medico': fields.float(u'Seguro Médico'),
        'decimo_tercero': fields.boolean(u'Décimo Tercero en rol', help="Marcar la casilla si el empleado recibirá el valor correspondiente al Décimo Tercer en el rol (usar 'decimo_tercero' en las formulas)"),
        'decimo_cuarto': fields.boolean(u'Décimo Cuarto en rol', help="Marcar la casilla si el empleado recibirá el valor correspondiente al Décimo Cuarto en el rol (usar 'decimo_cuarto' en las formulas)"),
        'trial_date_start': fields.date(u'Fecha inicio de periodo de prueba'),
        'trial_date_end': fields.date(u'Fecha final de periodo de prueba'),
        'firstyear_date_start': fields.date(u'Fecha inicio de primer año'),
        'firstyear_date_end': fields.date(u'Fecha final de primer año'),
        'activo': fields.boolean(u'Incluye en último rol?', help="Desactivar el casillero si no se debe generar el rol del último mes laborado"),
        'regimen': fields.selection([('s','Sierra'),('c','Costa')],u'Régimen', required=True),
        'centro_costo_id': fields.many2one('hr.centro_costo', u'Centro de Costo'),
        'hours_per_month': fields.integer(u'Horas por Mes'),
        'hours_per_week': fields.integer(u'Horas por Semana'),
        'codigo_ocupacional': fields.char(u'Código Ocupacional',size=20),
        'funciones_confianza': fields.boolean(u'Funciones Confianza'),
        'valor_adicional1': fields.float(u'Valor Adicional 1'),
        'valor_adicional2': fields.float(u'Valor Adicional 2'),
        'valor_adicional3': fields.float(u'Valor Adicional 3'),
        'valor_adicional4': fields.float(u'Valor Adicional 4'),
        'valor_adicional5': fields.float(u'Valor Adicional 5'),
        'coach_id': fields.many2one('hr.employee', u'Jefe'),
        'replace_id': fields.many2one('hr.employee', u'Reemplaza a'),
    }

    _defaults = {
        'fondo_reserva': True,
        'decimo_tercero': False,
        'decimo_cuarto': False,
        'funciones_confianza': False,
        'activo': True,
        'biweekly_percent': 0,
        'seguro_medico': 0,
        'hours_per_month': 0,
        'regimen': 's',
        'company_id': lambda self, cr, uid, ctx=None: self.pool.get('res.company')._company_default_get(cr, uid, 'hr.job', context=ctx),
    }

    def onchange_periodo_prueba(self, cr, uid, ids, fecha_prueba, context={}):
        res={}
        if fecha_prueba:
            fecha_prueba = datetime.datetime.strptime(fecha_prueba, "%Y-%m-%d")
            fecha_final = fecha_prueba + datetime.timedelta(days=89)
            res['value']={'trial_date_end':fecha_final}
        return res

    def onchange_empleado(self, cr, uid, ids, empleado, context={}):
        res={}
        if empleado:
            dato = self.pool.get("hr.employee").browse(cr, uid, empleado, context=context)
            res['value']={'name':dato.name}
        return res

    def onchange_department(self, cr, uid, ids, departamento, context={}):
        res={}
        if departamento:
            dato = self.pool.get("hr.department").browse(cr, uid, departamento, context=context)
            res['value']={'coach_id':dato.manager_id.id}
        return res

    def _grabar_sqlserver(self, cr, uid, tipo, id, valores):
        import pyodbc
        import sys
        #import pdb
        #pdb.set_trace()
        sql_dict= {'department_id': 'ID_AREA', 'job_id': 'ID_PSTO', 'bono_eficiencia': 'COD_INT', 'date_start': 'FECHA_INGRESO', 'wage':'SUELDO_BASICO', 'city_id':'LOCALIDAD', 'coach_id': 'ID_SPRV'}
        sql_dict_ext= {'date_end':'EP_FECHA_SALIDA', 'ep_aporta':'EP_APORTA'}
        #PRIMERO REALIZAR LOS CAMBIOS
        valores['EP_APORTA']='SI'
        if valores.has_key('department_id'):
            dato = self.pool.get('hr.department').browse(cr, uid, valores['department_id'])
            valores['department_id'] = dato.anterior_id
        if valores.has_key('job_id'):
            dato = self.pool.get('hr.job').browse(cr, uid, valores['job_id'])
            valores['job_id'] = dato.anterior_id
        if valores.has_key('city_id'):
            dato = self.pool.get('res.country.state.city').browse(cr, uid, valores['city_id'])
            valores['city_id'] = dato.name
        for key in valores.keys():
            if str(type(valores[key]))=="<type 'unicode'>":
                valores[key] = unicodedata.normalize('NFKD', valores[key]).encode('ascii','ignore')
        if valores.has_key('coach_id'):
            dato = self.pool.get('hr.employee').browse(cr, uid, valores['coach_id'])
            valores['coach_id'] = dato.anterior_id
        #escribimos sobre el empleado creado en el compers
        if tipo=='write':
          for key in sql_dict.keys():
           if valores.has_key(key):
            try:
                cnxn = pyodbc.connect('DSN=SQLS_LI;UID=odo;PWD=odo2233')
                cursor = cnxn.cursor()
                cursor.execute('update PERSONAS SET ' + sql_dict[key] + '=? WHERE id=?', (valores[key], id))
                cnxn.commit()
                cnxn.close()
            except pyodbc.Error, err:
                raise osv.except_osv("Error!", err)
            except osv.except_osv, err:
                raise osv.except_osv("Error!", err)
            except:
                raise osv.except_osv("Error!", sys.exc_info()[0])
          for key in sql_dict_ext.keys():
           if valores.has_key(key):
            try:
                cnxn = pyodbc.connect('DSN=SQLS_LI;UID=odo;PWD=odo2233')
                cursor = cnxn.cursor()
                cursor.execute('update EXT_PERSONA SET ' + sql_dict_ext[key] + '=? WHERE id=?', (valores[key], id))
                cnxn.commit()
                cnxn.close()
            except pyodbc.Error, err:
                raise osv.except_osv("Error!", err)
            except osv.except_osv, err:
                raise osv.except_osv("Error!", err)
            except:
                raise osv.except_osv("Error!", sys.exc_info()[0])

    def create(self, cr, uid, vals, context=None):
        anterior_id=self.pool.get('hr.employee').browse(cr, uid, vals['employee_id']).anterior_id
        res_id = super(l10n_ec_hr_contract, self).create(cr, uid, vals, context=context)
        self._grabar_sqlserver(cr, uid, 'write', anterior_id, vals.copy())
        return res_id

    def write(self, cr, uid, ids, vals, context=None):
        for this in self.browse(cr, uid, ids, context=context):
            #for valor in ['wage','department_id','job_id','centro_costo_id','city_id','company_id']:
            for valor in ['department_id','job_id','centro_costo_id','city_id','company_id']:
                if vals.has_key(valor):
                    #datos = {}
                    #datos_obj = {'name':0}
                    obj_log = self.pool.get("hr.contract.log")
                    datos = self.pool.get("hr.contract").read(cr, uid, this.id, [valor])
                    diccionario = {'department_id': 'hr.department',
                                   'job_id': 'hr.job',
                                   #'coach_id': 'hr.employee',
                                   'centro_costo_id': 'hr.centro_costo',
                                   'city_id': 'res.country.state.city',
                                   'company_id': 'res.company'}
                    if valor!='wage':
                        datos_obj = self.pool.get(diccionario[valor]).read(cr, uid, datos[valor][0], ['name'])
                    #import pdb
                    #pdb.set_trace()
                    #print datos
                    obj_log.create(cr, uid, {'contract_id':this.id,
                                             'name': valor,
                                             'date': context.has_key('fecha_actualizacion') and context['fecha_actualizacion'] or strftime("%Y-%m-%d"),
                                             'previous_value': valor=='wage' and datos[valor] or datos_obj['name'],
                                             'new_value': valor=='wage' and vals[valor] or self.pool.get(diccionario[valor]).read(cr, uid, vals[valor], ['name'])['name'],
                                             })
        res = super(l10n_ec_hr_contract, self).write(cr, uid, ids, vals, context=context)
        for this in self.browse(cr, uid, ids, context=context):
            if this.employee_id.servicios_complementarios==False:
                self._grabar_sqlserver(cr, uid, 'write', this.employee_id.anterior_id, vals.copy())
                #pass
        return res



l10n_ec_hr_contract()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
