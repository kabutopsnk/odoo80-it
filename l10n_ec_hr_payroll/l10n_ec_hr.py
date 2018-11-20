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
from openerp.tools.translate import _
from openerp import tools
import unicodedata
import datetime


class ec_hr_job(osv.osv):
    _inherit = 'hr.job'
    _order = 'name asc'

    _columns = {
        'active': fields.boolean(u'Activo'),
        'anterior_id': fields.integer(u'ID Anterior'),
    }

    _defaults = {
        'active': True,
    }

    def _grabar_sqlserver(self, tipo, id, valores):
        import pyodbc
        import sys
        sql_dict= {'active': 'STATUS', 'name': 'PUESTO', 'description': 'DESCRIPCION'}
        #PRIMERO REALIZAR LOS CAMBIOS
        if valores.has_key('active'):
            valores['active'] = valores['active']==True and 'A' or 'E'
        for key in valores.keys():
            if str(type(valores[key]))=="<type 'unicode'>":
                valores[key] = unicodedata.normalize('NFKD', valores[key]).encode('ascii','ignore')
        if tipo=='create':
            try:
                #cnxn = pyodbc.connect('DSN=SQLS_LI; UID=odo; PWD=odo2233')
                cnxn = pyodbc.connect('DSN=SQLS_LI;UID=odo;PWD=odo2233')
                cursor = cnxn.cursor()
                cursor.execute('insert into PUESTOS (ID, ID_ROL, PUESTO, STATUS, DESCRIPCION) VALUES (?, 1, ?, ?, ?)', (id, valores['name'], valores['active'], valores['description']))
                cnxn.commit()
                cnxn.close()
            except pyodbc.Error, err:
                raise osv.except_osv("Error!", err)
            except osv.except_osv, err:
                raise osv.except_osv("Error!", err)
            except:
                raise osv.except_osv("Error!", sys.exc_info()[0])
        if tipo=='write':
          for key in sql_dict.keys():
           if valores.has_key(key):
            try:
                cnxn = pyodbc.connect('DSN=SQLS_LI;UID=odo;PWD=odo2233')
                cursor = cnxn.cursor()
                cursor.execute('update PUESTOS SET ' + sql_dict[key] + '=? WHERE id=?', (valores[key], id))
                cnxn.commit()
                cnxn.close()
            except pyodbc.Error, err:
                raise osv.except_osv("Error!", err)
            except osv.except_osv, err:
                raise osv.except_osv("Error!", err)
            except:
                raise osv.except_osv("Error!", sys.exc_info()[0])
        if tipo=='unlink':
            try:
                cnxn = pyodbc.connect('DSN=SQLS_LI;UID=odo;PWD=odo2233')
                cursor = cnxn.cursor()
                cursor.execute('delete from PUESTOS WHERE id=?', (id))
                cnxn.commit()
                cnxn.close()
            except pyodbc.Error, err:
                raise osv.except_osv("Error!", err)
            except osv.except_osv, err:
                raise osv.except_osv("Error!", err)
            except:
                raise osv.except_osv("Error!", sys.exc_info()[0])

    def create(self, cr, uid, vals, context=None):
        cr.execute("select max(anterior_id) from hr_job")
        table = cr.fetchall()
        anterior_id=False
        for row in table:
            anterior_id = row and row[0] or False
        anterior_id = anterior_id and anterior_id+1 or 1
        vals['anterior_id'] = anterior_id
        res_id = super(ec_hr_job, self).create(cr, uid, vals, context=context)
        self._grabar_sqlserver('create', anterior_id, vals.copy())
        return res_id

    def write(self, cr, uid, ids, vals, context=None):
        res = super(ec_hr_job, self).write(cr, uid, ids, vals, context=context)
        for this in self.browse(cr, uid, ids, context=context):
            self._grabar_sqlserver('write', this.anterior_id, vals.copy())
        return res

    def unlink(self, cr, uid, ids, context=None):
        res = super(ec_hr_job, self).unlink(cr, uid, ids, vals, context=context)
        for this in self.browse(cr, uid, ids, context=context):
            self._grabar_sqlserver('unlink', this.anterior_id, {})
        return res

ec_hr_job()

class ec_hr_department(osv.osv):
    _inherit = 'hr.department'
    _order = 'name asc'

    _columns = {
        'active': fields.boolean(u'Activo'),
        'anterior_id': fields.integer(u'ID Anterior'),
    }

    _defaults = {
        'active': True,
    }

    def _grabar_sqlserver(self, cr, uid, tipo, id, valores):
        import pyodbc
        import sys
        sql_dict= {'active': 'STATUS', 'name': 'AREA', 'parent_id': 'ID_PADRE'}
        #PRIMERO REALIZAR LOS CAMBIOS
        if valores.has_key('active'):
            valores['active'] = valores['active']==True and 'A' or 'E'
        if valores.has_key('parent_id'):
            parent = self.browse(cr, uid, valores['parent_id'])
            valores['parent_id'] = parent.anterior_id
        for key in valores.keys():
            if str(type(valores[key]))=="<type 'unicode'>":
                valores[key] = unicodedata.normalize('NFKD', valores[key]).encode('ascii','ignore')
        if tipo=='create':
            try:
                cnxn = pyodbc.connect('DSN=SQLS_LI;UID=odo;PWD=odo2233')
                cursor = cnxn.cursor()
                cursor.execute('insert into AREAS (ID, ID_PADRE, AREA, STATUS, SUC_COD, ID_PROCESO) VALUES (?, ?, ?, ?, 1, 2)', (id, valores['parent_id'], valores['name'], valores['active']))
                cnxn.commit()
                cnxn.close()
            except pyodbc.Error, err:
                raise osv.except_osv("Error!", err)
            except osv.except_osv, err:
                raise osv.except_osv("Error!", err)
            except:
                raise osv.except_osv("Error!", sys.exc_info()[0])
        if tipo=='write':
          for key in sql_dict.keys():
           if valores.has_key(key):
            try:
                cnxn = pyodbc.connect('DSN=SQLS_LI;UID=odo;PWD=odo2233')
                cursor = cnxn.cursor()
                cursor.execute('update AREAS SET ' + sql_dict[key] + '=? WHERE id=?', (valores[key], id))
                cnxn.commit()
                cnxn.close()
            except pyodbc.Error, err:
                raise osv.except_osv("Error!", err)
            except osv.except_osv, err:
                raise osv.except_osv("Error!", err)
            except:
                raise osv.except_osv("Error!", sys.exc_info()[0])
        if tipo=='unlink':
            try:
                cnxn = pyodbc.connect('DSN=SQLS_LI;UID=odo;PWD=odo2233')
                cursor = cnxn.cursor()
                cursor.execute('delete from AREAS WHERE id=?', (id))
                cnxn.commit()
                cnxn.close()
            except pyodbc.Error, err:
                raise osv.except_osv("Error!", err)
            except osv.except_osv, err:
                raise osv.except_osv("Error!", err)
            except:
                raise osv.except_osv("Error!", sys.exc_info()[0])

    def create(self, cr, uid, vals, context=None):
        cr.execute("select max(anterior_id) from hr_department where anterior_id<>99999")
        table = cr.fetchall()
        anterior_id=False
        for row in table:
            anterior_id = row and row[0] or False
        anterior_id = anterior_id and anterior_id+1 or 1
        vals['anterior_id'] = anterior_id
        res_id = super(ec_hr_department, self).create(cr, uid, vals, context=context)
        self._grabar_sqlserver(cr, uid, 'create', anterior_id, vals.copy())
        return res_id

    def write(self, cr, uid, ids, vals, context=None):
        res = super(ec_hr_department, self).write(cr, uid, ids, vals, context=context)
        for this in self.browse(cr, uid, ids, context=context):
            if vals.has_key('manager_id'):
                obj_contract = self.pool.get('hr.contract')
                time_actual = datetime.datetime.today()
                contrato_ids = obj_contract.search(cr, uid, [('department_id','=',this.id),
                                                             ('employee_id','!=',vals['manager_id']),
                                                             ('date_start','<=',str(time_actual)),
                                                             '|',
                                                             ('date_end','>=',str(time_actual)),
                                                             ('date_end','=',False)])
                obj_contract.write(cr, uid, contrato_ids, {'coach_id':vals['manager_id']})
                #import pdb
                #pdb.set_trace()
            self._grabar_sqlserver(cr, uid, 'write', this.anterior_id, vals.copy())
        return res

    def unlink(self, cr, uid, ids, context=None):
        res = super(ec_hr_department, self).unlink(cr, uid, ids, vals, context=context)
        for this in self.browse(cr, uid, ids, context=context):
            self._grabar_sqlserver(cr, uid, 'unlink', this.anterior_id, {})
        return res

ec_hr_department()

class ec_hr_centro_costo(osv.osv):
    _name = 'hr.centro_costo'
    _description = 'Centro de Costo utilizado para exportar Rol de Pagos'
    _order = 'code asc'

    _columns = {
        'code': fields.char(u'Código', size=24, required=True),
        'name': fields.char(u'Centro de Costo', size=100, required=True),
    }

    _sql_constraints = [
        ('code_uniq', 'unique(code)', u'El código del centro de costo debe ser único'),
    ]
    
    def name_get(self, cr, uid, ids, context={}):
        if not ids:
            return []
        try:
            flag = len(ids)
        except:
            ids = [ids]
        res = []
        reads = self.browse(cr, uid, ids, context=context)
        for record in reads:
            name = "[" + record.code + "] " + record.name
            res.append((record.id, name))
        return res
    
    def name_search(self, cr, uid, name='', args=[], operator='ilike', context={}, limit=80):
        ids = []
        ids_nombre = self.search(cr, uid, [('name', operator, name)] + args, limit=limit, context=context)
        ids = list(set(ids + ids_nombre))
        if name:
            ids_cedula = self.search(cr, uid, [('code', operator, name)] + args, limit=limit, context=context)
            ids = list(set(ids + ids_cedula))
        return self.name_get(cr, uid, ids, context=context)

ec_hr_centro_costo()

class ec_hr_cuenta_contable(osv.osv):
    _name = 'hr.cuenta_contable'
    _description = 'Cuenta Contable utilizada para exportar Rol de Pagos'
    _order = 'code asc'

    _columns = {
        'code': fields.char(u'Código', size=24, required=True),
        'name': fields.char(u'Cuenta Contable', size=200, required=True),
    }

    _sql_constraints = [
        ('code_uniq', 'unique(code)', u'El código de la cuenta contable debe ser único'),
    ]
    
    def name_get(self, cr, uid, ids, context={}):
        if not ids:
            return []
        try:
            flag = len(ids)
        except:
            ids = [ids]
        res = []
        reads = self.browse(cr, uid, ids, context=context)
        for record in reads:
            name = "[" + record.code + "] " + record.name
            res.append((record.id, name))
        return res
    
    def name_search(self, cr, uid, name='', args=[], operator='ilike', context={}, limit=80):
        ids = []
        ids_nombre = self.search(cr, uid, [('name', operator, name)] + args, limit=limit, context=context)
        ids = list(set(ids + ids_nombre))
        if name:
            ids_cedula = self.search(cr, uid, [('code', operator, name)] + args, limit=limit, context=context)
            ids = list(set(ids + ids_cedula))
        return self.name_get(cr, uid, ids, context=context)

ec_hr_cuenta_contable()

class ec_hr_grupos_cuentas(osv.osv):
    _name = 'hr.grupos_cuentas'
    _description = 'Grupos Contables utilizada para exportar Rol de Pagos'
    _order = 'code asc'

    _columns = {
        'code': fields.char(u'Código', size=24, required=True),
        'name': fields.char(u'Grupo', size=100, required=True),
        'cuenta': fields.many2one('hr.cuenta_contable', u'Cuenta Acumulación', help='Coloque un numero de cuenta en este casillero en caso que todo el rubro se acumule en ella, sin diferenciar el Centro de Costo.'),
        'cuenta_sobregiro': fields.many2one('hr.cuenta_contable', u'Cuenta Sobregiro', help='Coloque un numero de cuenta en este casillero en caso que el rubro sea menor a cero, sin diferenciar el Centro de Costo.'),
        'line_ids': fields.one2many('hr.grupos_linea', 'grupo_id', u'Detalle'),
    }
    
    def name_get(self, cr, uid, ids, context={}):
        if not ids:
            return []
        try:
            flag = len(ids)
        except:
            ids = [ids]
        res = []
        reads = self.browse(cr, uid, ids, context=context)
        for record in reads:
            name = "[" + record.code + "] " + record.name
            res.append((record.id, name))
        return res
    
    def name_search(self, cr, uid, name='', args=[], operator='ilike', context={}, limit=80):
        ids = []
        ids_nombre = self.search(cr, uid, [('name', operator, name)] + args, limit=limit, context=context)
        ids = list(set(ids + ids_nombre))
        if name:
            ids_cedula = self.search(cr, uid, [('code', operator, name)] + args, limit=limit, context=context)
            ids = list(set(ids + ids_cedula))
        return self.name_get(cr, uid, ids, context=context)

ec_hr_grupos_cuentas()

class ec_hr_grupos_linea(osv.osv):
    _name = 'hr.grupos_linea'
    _description = 'Detalle del Grupo Contable utilizado para exportar Rol de Pagos'
    _order = 'centro_costo_id asc'

    _columns = {
                'grupo_id': fields.many2one('hr.grupos_cuentas', u'Grupo de cuentas', required=True, ondelete='cascade'),
                'centro_costo_id': fields.many2one('hr.centro_costo', u'Centro Costo', required=True),
                'cuenta': fields.many2one('hr.cuenta_contable', u'Cuenta', required=True),
                #'cuenta_haber': fields.many2one('hr.cuenta_contable', u'Cuenta Haber'),
    }

ec_hr_grupos_linea()

#FUNCIONES VARIAS PARA AYUDA

class compers_employee_family(osv.osv_memory):
    _name = 'compers.employee.family'
    _description = 'Actualizar cargas familiares que no existen en el compers'

    _columns = {
                'name': fields.char('Actualizar:', required=True),
    }

    _defaults = {
                'name': 'SOLO REGISTROS NO EXISTENTES EN COMPERS',
    }


    def actualizar_compers(self, cr, uid, ids, context={}):
        obj_empleado = self.pool.get('hr.employee')
        obj_contrato = self.pool.get('hr.contract')
        empleados_activos = []
        time_actual = datetime.datetime.today()
        ids_contratos = obj_contrato.search(cr, uid, [('date_start','<=',str(time_actual)),
                                                      '|',
                                                      ('date_end','>',str(time_actual)),
                                                      ('date_end','=',False)])
        for contrato in obj_contrato.browse(cr, uid, ids_contratos, context):
            empleados_activos.append(contrato.employee_id.id)
        servicios_complementarios = obj_empleado.search(cr, uid, [('servicios_complementarios','=',True)])
        empleados_ids = list(set(empleados_activos + servicios_complementarios))
        empleados_inactivos = obj_empleado.search(cr, uid, [('id','not in',empleados_ids)])
        #import pdb
        #pdb.set_trace()
        obj_empleado.write(cr, uid, empleados_activos, {'active':True})
        return obj_empleado.write(cr, uid, empleados_inactivos, {'active':False})

    def actualizar_compers_anteriorrr(self, cr, uid, ids, context={}):
        import pyodbc
        import sys
        obj_family = self.pool.get('hr.employee.family')
        family_ids = obj_family.search(cr, uid, [], context=context)
        for familiar in obj_family.browse(cr, uid, family_ids, context=context):
            cnxn = pyodbc.connect('DSN=SQLS_LI;UID=odo;PWD=odo2233')
            cursor = cnxn.cursor()
            #import pdb
            #pdb.set_trace()
            cursor.execute('select CAF_COD, ID from CARGAS_FAMI where CAF_COD=' + str(familiar.anterior_id) + ' and ID=' + str(familiar.employee_id.anterior_id))
            tabla = cursor.fetchall()
            if not tabla:
                BLOOD = {'on':'O-','op':'O+','an':'A-','ap':'A+','bn':'B-','bp':'B+','abn':'AB-','abp':'AB+'}
                sql_dict= {'ID': familiar.employee_id.anterior_id,
                           'CAF_COD': familiar.anterior_id,
                           'CAF_NOMBRE': familiar.name,
                           'PARE_COD': familiar.relationship_id.anterior_id,
                           'CAF_CEDULA': familiar.identifier,
                           'CAF_FECHA_NAC': familiar.birthday,
                           'CAF_DISCAPACIDAD': familiar.disability_id and familiar.disability_id.anterior_id or 0,
                           'DISCAPACIDAD': familiar.disability_id.anterior_id,
                           'CAF_SEXO': familiar.gender[:1].upper(),
                           'CAF_ESTADO_CIVIL': familiar.marital_id.name,
                           'CAF_OCUPACION': familiar.occupation,
                           'CAF_DIRECCION': familiar.address,
                           'CAF_TELEFONO': familiar.phone,
                           'CAF_MAIL': familiar.email,
                           'CAF_SANGRE': familiar.blood_type and BLOOD[familiar.blood_type] or '',
                           'CAF_MINISUVALI': familiar.disabled==True and 'S' or 'N',
                           'CAF_EST_ESTUDI': familiar.student==True and 'S' or 'N',
                           'CAF_EST_FAMILI': 'N',
                           'CAF_EST_UTILIDAD': 'S',
                           }
                for key in sql_dict.keys():
                    if str(type(sql_dict[key]))=="<type 'unicode'>":
                        sql_dict[key] = unicodedata.normalize('NFKD', sql_dict[key]).encode('ascii','ignore')
                try:
                    cnxn = pyodbc.connect('DSN=SQLS_LI;UID=odo;PWD=odo2233')
                    cursor = cnxn.cursor()
                    cursor.execute("""insert into CARGAS_FAMI (CAF_COD,
                                                               ID,
                                                               CAF_NOMBRE,
                                                               PARE_COD,
                                                               CAF_CEDULA,
                                                               CAF_FECHA_NAC,
                                                               CAF_DISCAPACIDAD,
                                                               CAF_SEXO,
                                                               CAF_ESTADO_CIVIL,
                                                               CAF_OCUPACION,
                                                               CAF_DIRECCION,
                                                               CAF_TELEFONO,
                                                               CAF_MAIL,
                                                               CAF_SANGRE,
                                                               CAF_MINISUVALI,
                                                               CAF_EST_ESTUDI,
                                                               CAF_EST_FAMILI,
                                                               CAF_EST_UTILIDAD)
                                                               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                                                               (sql_dict['CAF_COD'],
                                                                sql_dict['ID'],
                                                                sql_dict['CAF_NOMBRE'],
                                                                sql_dict['PARE_COD'],
                                                                sql_dict['CAF_CEDULA'],
                                                                sql_dict['CAF_FECHA_NAC'],
                                                                sql_dict['CAF_DISCAPACIDAD'],
                                                                sql_dict['CAF_SEXO'],
                                                                sql_dict['CAF_ESTADO_CIVIL'],
                                                                sql_dict['CAF_OCUPACION'],
                                                                sql_dict['CAF_DIRECCION'],
                                                                sql_dict['CAF_TELEFONO'],
                                                                sql_dict['CAF_MAIL'],
                                                                sql_dict['CAF_SANGRE'],
                                                                sql_dict['CAF_MINISUVALI'],
                                                                sql_dict['CAF_EST_ESTUDI'],
                                                                sql_dict['CAF_EST_FAMILI'],
                                                                sql_dict['CAF_EST_UTILIDAD'],))
                    cnxn.commit()
                    cnxn.close()
                except pyodbc.Error, err:
                    raise osv.except_osv("Error!", err)
                except osv.except_osv, err:
                    raise osv.except_osv("Error!", err)
                except:
                    raise osv.except_osv("Error!", sys.exc_info()[0])


compers_employee_family()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
