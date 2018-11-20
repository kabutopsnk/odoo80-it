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
from time import strftime
import unicodedata
import exceptions

class l10n_ec_hr_marital_status(osv.osv):
    _name = 'hr.marital.status'
    _description = 'Tipo de estado civil de una persona'
    _order = 'name asc'

    _columns = {
        'name': fields.char(u'Estado Civil', size=30, required=True),
    }

l10n_ec_hr_marital_status()

class l10n_ec_hr_employee_disability(osv.osv):
    _name = 'hr.employee.disability'
    _description = 'Tipo de discapacidad de una persona'
    _order = 'name desc'

    _columns = {
        'name': fields.char(u'Tipo de discapacidad', size=50, required=True),
        'active': fields.boolean(u'Activo'),
        'anterior_id': fields.integer(u'ID Anterior'),
    }

    _defaults = {
        'active': True,
    }
    
    def _grabar_sqlserver(self, tipo, id, valores):
        import pyodbc
        import sys
        sql_dict= {'active': 'STATUS', 'name': 'NOMBRE'}
        #PRIMERO REALIZAR LOS CAMBIOS
        if valores.has_key('active'):
            valores['active'] = valores['active']==True and 'A' or 'E'
        for key in valores.keys():
            if str(type(valores[key]))=="<type 'unicode'>":
                #valores[key] = = str (valores[key])
                valores[key] = unicodedata.normalize('NFKD', valores[key]).encode('ascii','ignore')
        if tipo=='create':
            try:
                cnxn = pyodbc.connect('DSN=SQLS_LI;UID=odo;PWD=odo2233')
                cursor = cnxn.cursor()
                cursor.execute('insert into DISCAPACIDAD (ID, NOMBRE, STATUS) VALUES (?, ?, ?)', (id, valores['name'], valores['active']))
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
                cursor.execute('update DISCAPACIDAD SET ' + sql_dict[key] + '=? WHERE id=?', (valores[key], id))
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
                cursor.execute('delete from DISCAPACIDAD WHERE id=?', (id))
                cnxn.commit()
                cnxn.close()
            except pyodbc.Error, err:
                raise osv.except_osv("Error!", err)
            except osv.except_osv, err:
                raise osv.except_osv("Error!", err)
            except:
                raise osv.except_osv("Error!", sys.exc_info()[0])

    def create(self, cr, uid, vals, context=None):
        cr.execute("select max(anterior_id) from hr_employee_disability")
        table = cr.fetchall()
        anterior_id=False
        for row in table:
            anterior_id = row and row[0] or False
        anterior_id = anterior_id and anterior_id+1 or 1
        vals['anterior_id'] = anterior_id
        res_id = super(l10n_ec_hr_employee_disability, self).create(cr, uid, vals, context=context)
        self._grabar_sqlserver('create', anterior_id, vals.copy())
        return res_id

    def write(self, cr, uid, ids, vals, context=None):
        res = super(l10n_ec_hr_employee_disability, self).write(cr, uid, ids, vals, context=context)
        for this in self.browse(cr, uid, ids, context=context):
            self._grabar_sqlserver('write', this.anterior_id, vals.copy())
        return res

    def unlink(self, cr, uid, ids, context=None):
        for this in self.browse(cr, uid, ids, context=context):
            self._grabar_sqlserver('unlink', this.anterior_id, {})
        res = super(l10n_ec_hr_employee_disability, self).unlink(cr, uid, ids, context=context)
        return res

l10n_ec_hr_employee_disability()

class l10n_ec_hr_employee_reference(osv.osv):
    _name = 'hr.employee.reference'
    _description = 'Referencias personales de un Empleado'
    _order = 'name desc'

    _columns = {
        'employee_id':  fields.many2one('hr.employee', u'Empleado', required=True),
        'name': fields.char(u'Nombre', size=50, required=True),
        'phone': fields.char(u'Teléfono', size=30, required=True),
        'email': fields.char(u'Email', size=50),
    }

l10n_ec_hr_employee_reference()

class ec_hr_employee_experience_sector(osv.osv):
    _name = 'hr.employee.experience.sector'
    _description = 'Sector de la Experiencia Laboral de un empleado'
    _order = 'name asc'

    _columns = {
        'name': fields.char(u'Sector Laboral', size=50, required=True),
    }

ec_hr_employee_experience_sector()

class ec_hr_employee_experience_institution(osv.osv):
    _name = 'hr.employee.experience.institution'
    _description = 'Experiencia laboral en instituciones de tipo'
    _order = 'name asc'

    _columns = {
        'name': fields.char(u'Experiencia en instituciones de tipo', size=50, required=True),
    }

ec_hr_employee_experience_institution()

class ec_hr_employee_experience_job(osv.osv):
    _name = 'hr.employee.experience.job'
    _description = 'Experiencia laboral en cargos de tipo'
    _order = 'name asc'

    _columns = {
        'name': fields.char(u'Experiencia en cargos de tipo', size=50, required=True),
    }

ec_hr_employee_experience_job()

class ec_hr_employee_experience(osv.osv):
    _name = 'hr.employee.experience'
    _description = 'Experiencia Laboral de un Empleado'

    _columns = {
        'employee_id':  fields.many2one('hr.employee', u'Empleado', required=True),
        'anterior_id': fields.integer(u'ID Anterior'),
        'institution': fields.char(u'Institución', size=100),
        'job': fields.char(u'Cargo', size=100),
        'sector_id': fields.many2one('hr.employee.experience.sector', u'Sector'),
        'date_start': fields.date(u'Fecha de ingreso'),
        'date_stop': fields.date(u'Fecha de salida'),
        'experience_institution_id': fields.many2one('hr.employee.experience.institution', u'Experiencia en instituciones de tipo'),
        'experience_job_id': fields.many2one('hr.employee.experience.job', u'Experiencia en cargos de tipo'),
        'description': fields.char(u'Descripción', size=200),
        'reference_name': fields.char(u'Nombre de la ref.', size=100),
        'reference_institution': fields.char(u'Institución de ref.', size=100),
        'reference_job': fields.char(u'Cargo de la ref.', size=100),
        'reference_phone': fields.char(u'Teléfono de la ref.', size=30),
    }

    def _grabar_sqlserver(self, cr, uid, tipo, id, empleado_id, valores):
        import pyodbc
        import sys
        sql_dict= {'employee_id': 'id_PERSO',
                   'job': 'CARGO',
                   'date_start': 'FECHA_INI',
                   'date_stop': 'FECHA_FIN',
                   'institution': 'INSTITUCION',
                   'sector_id': 'TIPO',
                   'reference_name': 'NOMBRE_REF',
                   'reference_institution': 'EMPRESA_REF',
                   'reference_job': 'CARGO_REF',
                   'reference_phone': 'TELEFONO_REF',
                   'experience_institution_id': 'EXPE_INSTITUCION',
                   'experience_job_id': 'EXPE_CARGO',
                   'description': 'DESCRIPCION'}
        #PRIMERO REALIZAR LOS CAMBIOS
        if valores.has_key('employee_id'):
            dato = self.pool.get('hr.employee').browse(cr, uid, valores['employee_id'])
            valores['employee_id'] = dato.anterior_id
        else:
            valores['employee_id'] = empleado_id
        if valores.has_key('sector_id'):
            dato = self.pool.get('hr.employee.experience.sector').browse(cr, uid, valores['sector_id'])
            valores['sector_id'] = dato.name
        if valores.has_key('experience_institution_id'):
            dato = self.pool.get('hr.employee.experience.institution').browse(cr, uid, valores['experience_institution_id'])
            valores['experience_institution_id'] = dato.name
        if valores.has_key('experience_job_id'):
            dato = self.pool.get('hr.employee.experience.job').browse(cr, uid, valores['experience_job_id'])
            valores['experience_job_id'] = dato.name
        for key in valores.keys():
            #print str(type(valores[key])) + ": " + str(key) + " ; " + str(valores[key])
            if str(type(valores[key]))=="<type 'unicode'>":
                valores[key] = unicodedata.normalize('NFKD', valores[key]).encode('ascii','ignore')
                #print "modificado"
        #import pdb
        #pdb.set_trace()
        if tipo=='create':
            try:
                cnxn = pyodbc.connect('DSN=SQLS_LI;UID=odo;PWD=odo2233')
                cursor = cnxn.cursor()
                cursor.execute('insert into PERSO_expe (ID, ID_PERSO, CARGO, FECHA_INI, FECHA_FIN, INSTITUCION, TIPO, NOMBRE_REF, EMPRESA_REF, CARGO_REF, TELEFONO_REF, EXPE_INSTITUCION, EXPE_CARGO, DESCRIPCION) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (id, valores['employee_id'], str(valores['job']), valores['date_start'], valores['date_stop'], valores['institution'], valores['sector_id'], valores['reference_name'], valores['reference_institution'], valores['reference_job'], valores['reference_phone'], valores['experience_institution_id'], valores['experience_job_id'], valores['description']))
                cnxn.commit()
                cnxn.close()
            except pyodbc.Error, err:
                raise osv.except_osv("Error!", err)
            except osv.except_osv, err:
                raise osv.except_osv("Error!", err)
            except exceptions.KeyError, err:
                raise osv.except_osv("Error!", err)
            except:
                raise osv.except_osv("Error!", sys.exc_info()[0])
        if tipo=='write':
          for key in sql_dict.keys():
           if valores.has_key(key):
            try:
                cnxn = pyodbc.connect('DSN=SQLS_LI;UID=odo;PWD=odo2233')
                cursor = cnxn.cursor()
                cursor.execute('update PERSO_EXPE SET ' + sql_dict[key] + '=? WHERE id=? and id_perso=?', (valores[key], id, valores['employee_id']))
                cnxn.commit()
                cnxn.close()
            except pyodbc.Error, err:
                raise osv.except_osv("Error!", err)
            except osv.except_osv, err:
                raise osv.except_osv("Error!", err)
            except exceptions.KeyError, err:
                raise osv.except_osv("Error!", err)
            except:
                raise osv.except_osv("Error!", sys.exc_info()[0])
        if tipo=='unlink':
            try:
                cnxn = pyodbc.connect('DSN=SQLS_LI;UID=odo;PWD=odo2233')
                cursor = cnxn.cursor()
                cursor.execute('delete from PERSO_EXPE WHERE id=? and id_perso=?', (id, valores['employee_id']))
                cnxn.commit()
                cnxn.close()
            except pyodbc.Error, err:
                raise osv.except_osv("Error!", err)
            except osv.except_osv, err:
                raise osv.except_osv("Error!", err)
            except:
                raise osv.except_osv("Error!", sys.exc_info()[0])

    def create(self, cr, uid, vals, context=None):
        cr.execute("select max(anterior_id) from hr_employee_experience where employee_id="+str(vals['employee_id']))
        table = cr.fetchall()
        anterior_id=False
        for row in table:
            anterior_id = row and row[0] or False
        anterior_id = anterior_id and anterior_id+1 or 1
        vals['anterior_id'] = anterior_id
        res_id = super(ec_hr_employee_experience, self).create(cr, uid, vals, context=context)
        empleado = self.pool.get('hr.employee').browse(cr, uid, vals['employee_id'])
        self._grabar_sqlserver(cr, uid, 'create', anterior_id, empleado.anterior_id, vals.copy())
        return res_id

    def write(self, cr, uid, ids, vals, context=None):
        res = super(ec_hr_employee_experience, self).write(cr, uid, ids, vals, context=context)
        for this in self.browse(cr, uid, ids, context=context):
            self._grabar_sqlserver(cr, uid, 'write', this.anterior_id, this.employee_id.anterior_id, vals.copy())
        return res

    def unlink(self, cr, uid, ids, context=None):
        for this in self.browse(cr, uid, ids, context=context):
            self._grabar_sqlserver(cr, uid, 'unlink', this.anterior_id, this.employee_id.anterior_id, {})
        res = super(ec_hr_employee_experience, self).unlink(cr, uid, ids, context=context)
        return res

ec_hr_employee_experience()

class l10n_ec_hr_employee_family_type(osv.osv):
    _name = 'hr.employee.family.type'
    _description = 'Relacion familiar a un empleado'
    _order = 'name desc'

    _columns = {
        'anterior_id': fields.integer(u'ID Anterior'),
        'name': fields.char(u'Relación Familiar', size=50, required=True),
    }

l10n_ec_hr_employee_family_type()

class l10n_ec_hr_employee_projection(osv.osv):
    _name = 'hr.employee.projection'
    _description='Proyeccion de gastos personales de un empleado'

    def _compute_all(self, cr, uid, id, name, args, context):
        result={}
        for anual in self.browse(cr, uid, id):
            sum=0
            for line in anual.line_ids:
                sum+=line.value
            result[anual.id]=sum
        return result

    _columns = {
        'name': fields.char(u'Descripción', size=64),
        'date_start': fields.date(u'Fecha de inicio'),
        'date_stop': fields.date(u'Fecha fin'),
        'line_ids': fields.one2many('hr.employee.projection.line','projection_id',u'Lineas Proyección'),
        'employee_id': fields.many2one('hr.employee',u'Empleado', ondelete='cascade'),
        'total': fields.function(_compute_all, method=True, string=u'Total', type='float', readonly=True),
    }

    _defaults = {
        'name': 'Proyeccion de gastos',
               }

l10n_ec_hr_employee_projection()

class l10n_ec_hr_employee_projection_line(osv.osv):
    
    _name='hr.employee.projection.line'
    _description='Detalle de proyeccion de gastos personales de un empleado'

    _columns = {
        'name': fields.many2one('hr.expenses',u'Tipo de gasto'),
        'value': fields.float(u'Valor'),
        'projection_id': fields.many2one('hr.employee.projection', u'Año', ondelete='cascade'),
        }

l10n_ec_hr_employee_projection_line()

class l10n_ec_hr_employee_profit(osv.osv):
    _name = 'hr.employee.profit'
    _description='Rentabilidad anual del empleado'

    #def _compute_all(self, cr, uid, id, name, args, context):
    #    sum=0
    #    result={}
    #    for anual in self.browse(cr, uid, id):
    #        for line in anual.line_ids:
    #            sum+=line.value
    #        result[anual.id]=sum
    #    return result

    _columns = {
        'name': fields.char(u'Descripción', size=64),
        'date_start': fields.date(u'Fecha de inicio'),
        'date_stop': fields.date(u'Fecha fin'),
        'line_ids': fields.one2many('hr.employee.profit.line','profit_id',u'Detalle'),
        'employee_id': fields.many2one('hr.employee',u'Empleado', ondelete='cascade'),
        #'total': fields.function(_compute_all, method=True, string='Total', type='float', readonly=True),
    }

    _defaults = {
        'name': 'Resumen ',
               }

    _order = "employee_id asc"

l10n_ec_hr_employee_profit()

class l10n_ec_hr_employee_profit_line(osv.osv):
    
    _name='hr.employee.profit.line'
    _description='Detalle de rentabilidad anual de empleado'

    _columns = {
        'name': fields.selection([('mensual','Mensual'),('utilidades','Utilidades'),('decimotercero','Decimo Tercero'),('decimocuarto','Decimo Cuarto'),('otro','Otro')], u'Tipo', readonly=True),
        'date_start': fields.date(u'Fecha de inicio'),
        'date_stop': fields.date(u'Fecha fin'),
        'profit_id': fields.many2one('hr.employee.profit', u'Año', ondelete='cascade'),
        'proyectar_aportable':fields.float(u'Proyectable - Aportable'),
        'proyectar_no_aportable':fields.float(u'Proyectable - No aportable'),
        'no_proyectar_aportable':fields.float(u'No proyectable - Aportable'),
        'no_proyectar_no_aportable':fields.float(u'No proyectable - No aportable'),
        'retenido':fields.float(u'Valor retenido'),
        'otros_empleadores':fields.float(u'Otros empleadores'),
        'otros_empleadores_iess':fields.float(u'Aporte IESS otros empleadores'),
        'otros_empleadores_retenido':fields.float(u'Retenido por otros empleadores'),
        'otros_valores':fields.float(u'Otros'),
        }

    _defaults = {
        'name': 'otro',
        'proyectar_aportable':0,
        'proyectar_no_aportable':0,
        'no_proyectar_aportable':0,
        'no_proyectar_no_aportable':0,
        'otros_empleadores':0,
        'otros_empleadores_iess':0,
        'otros_empleadores_retenido':0,
        'otros_valores':0,
        }

l10n_ec_hr_employee_profit_line()

class l10n_ec_hr_employee_family(osv.osv):
    _name = 'hr.employee.family'
    _description = 'Familiares de empleado'
    _order = 'name desc'

    _BLOOD = [('on','O-'),('op','O+'),('an','A-'),('ap','A+'),
              ('bn','B-'),('bp','B+'),('abn','AB-'),('abp','AB+')]
            
    _columns = {
        'name': fields.char(u'Nombre completo', size=50, required=True),
        'anterior_id': fields.integer(u'ID Anterior'),
        'relationship_id': fields.many2one('hr.employee.family.type', u'Parentesco', required=True),
        'identifier': fields.char(u'Identificador', size=15),
        'gender': fields.selection([('male', 'Hombre'),('female', 'Mujer')], u'Género'),
        'marital_id': fields.many2one('hr.marital.status',u'Estado Civil'),
        'blood_type':  fields.selection(_BLOOD,u'Tipo de sangre'),
        'birthday': fields.date(u'Fecha de Nacimiento'),
        #'disabled': fields.boolean(u'Discapacitado?', help=u"Marque este campo si la carga familiar tiene alguna limitación para llevar a cabo ciertas actividades provocadas por una deficiencia física o mental"),
        'student': fields.boolean(u'Es estudiante?'),
        'disability_id': fields.many2one('hr.employee.disability',u'Tipo de discapacidad'),
        'disability_percent': fields.float(u'Porcentaje de discapacidad'),
        'id_disability': fields.char(u'ID CONADIS', size=15, help=u"Codigo de identificación del CONADIS"),
        'employee_id':  fields.many2one('hr.employee', u'Empleado', required=True),
        #'recibe_pension': fields.selection([('pension_alimenticia',u'Pensión Alimenticia'),('funcion_judicial',u'Función Judicial')],u'Recibe pensión?', help=u'Activar este campo en caso que esta carga familiar reciba pensión alimenticia y elija el tipo de descuento'),
        #'valor_pension': fields.float(u'Valor del descuento', help=u'Valor a descontar al empleado por la pensión'),
        'address': fields.char(u'Dirección', size=100),
        'phone': fields.char(u'Teléfono', size=30),
        'occupation': fields.char(u'Ocupación', size=30),
        'email': fields.char(u'Email', size=50),
        }

    def _grabar_sqlserver(self, cr, uid, tipo, id, empleado_id, valores):
        import pyodbc
        import sys #CAF_COD
        sql_dict= {'employee_id': 'ID',
                   'name': 'CAF_NOMBRE',
                   'relationship_id': 'PARE_COD',
                   'identifier': 'CAF_CEDULA',
                   'birthday': 'CAF_FECHA_NAC',
                   'disability_id': 'CAF_DISCAPACIDAD',
                   'discapacidad': 'DISCAPACIDAD',
                   'gender': 'CAF_SEXO',
                   'marital_id': 'CAF_ESTADO_CIVIL',
                   'occupation': 'CAF_OCUPACION',
                   'address': 'CAF_DIRECCION',
                   'phone': 'CAF_TELEFONO',
                   'email': 'CAF_MAIL',
                   'blood_type': 'CAF_SANGRE',
                   'disabled': 'CAF_MINISUVALI', #CAF_EST_FAMILI N
                   'student': 'CAF_EST_ESTUDI', #CAF_EST_UTILIDAD S
                   }
        #PRIMERO REALIZAR LOS CAMBIOS
        if valores.has_key('employee_id'):
            dato = self.pool.get('hr.employee').browse(cr, uid, valores['employee_id'])
            valores['employee_id'] = dato.anterior_id
        else:
            valores['employee_id'] = empleado_id
        if valores.has_key('student'):
            valores['student'] = valores['student']==True and 'S' or 'N'
        #if valores.has_key('disabled'):
        #    valores['disabled'] = valores['disabled']==True and 'S' or 'N'
        if valores.has_key('country_id'):
            dato = self.pool.get('res.country').browse(cr, uid, valores['country_id'])
            valores['country_id'] = dato.code_phone
            valores['pais'] = dato.name.upper()
        if valores.has_key('relationship_id'):
            dato = self.pool.get('hr.employee.family.type').browse(cr, uid, valores['relationship_id'])
            valores['relationship_id'] = dato.anterior_id
        if valores.has_key('email'):
          if not valores['email']:
            valores['email'] = ''
        if valores.has_key('disability_id'):
          if valores['disability_id']:
            dato = self.pool.get('hr.employee.disability').browse(cr, uid, valores['disability_id'])
            valores['disability_id'] = dato.anterior_id
            valores['disabled'] = dato.anterior_id==0 and 'N' or 'S'
          else:
            valores['disability_id'] = 1
            valores['disabled'] = 'N'
        else:
            valores['disability_id'] = 1
            valores['disabled'] = 'N'
        if valores.has_key('gender'):
            valores['gender'] = valores['gender'][:1].upper()
        if valores.has_key('marital_id'):
            dato = self.pool.get('hr.marital.status').browse(cr, uid, valores['marital_id'])
            valores['marital_id'] = dato.name
        if valores.has_key('blood_type'):
          if valores['blood_type']:
            BLOOD = {'on':'O-','op':'O+','an':'A-','ap':'A+','bn':'B-','bp':'B+','abn':'AB-','abp':'AB+'}
            valores['blood_type'] = BLOOD[valores['blood_type']]
        for key in valores.keys():
            #print str(type(valores[key])) + ": " + str(key) + " ; " + str(valores[key])
            if str(type(valores[key]))=="<type 'unicode'>":
                valores[key] = unicodedata.normalize('NFKD', valores[key]).encode('ascii','ignore')
                #print "modificado"
        #import pdb
        #pdb.set_trace()
        if tipo=='create':
            try:
                cnxn = pyodbc.connect('DSN=SQLS_LI;UID=odo;PWD=odo2233')
                cursor = cnxn.cursor()
                cursor.execute('insert into CARGAS_FAMI (CAF_COD, ID, CAF_NOMBRE, PARE_COD, CAF_CEDULA, CAF_FECHA_NAC, CAF_DISCAPACIDAD, CAF_SEXO, CAF_ESTADO_CIVIL, CAF_OCUPACION, CAF_DIRECCION, CAF_TELEFONO, CAF_MAIL, CAF_SANGRE, CAF_MINISUVALI, CAF_EST_ESTUDI, CAF_EST_FAMILI, CAF_EST_UTILIDAD) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (id, valores['employee_id'], valores['name'], valores['relationship_id'], valores['identifier'], valores['birthday'], valores.has_key('disability_id') and valores['disability_id'] or 1, valores['gender'], valores['marital_id'], valores['occupation'], valores['address'], valores['phone'], valores.has_key('email') and valores['email'] or '', valores.has_key('blood_type') and valores['blood_type'] or '', valores.has_key('disabled') and valores['disabled'] or '', valores.has_key('student') and valores['student'] or '', 'N', 'S'))
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
                cursor.execute('update CARGAS_FAMI SET ' + sql_dict[key] + '=? WHERE CAF_COD=? and id=?', (valores[key], id, valores['employee_id']))
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
                cursor.execute('delete from CARGAS_FAMI WHERE CAF_COD=? and id=?', (id, valores['employee_id']))
                cnxn.commit()
                cnxn.close()
            except pyodbc.Error, err:
                raise osv.except_osv("Error!", err)
            except osv.except_osv, err:
                raise osv.except_osv("Error!", err)
            except:
                raise osv.except_osv("Error!", sys.exc_info()[0])

    def create(self, cr, uid, vals, context=None):
        cr.execute("select max(anterior_id) from hr_employee_family where employee_id="+str(vals['employee_id']))
        table = cr.fetchall()
        anterior_id=False
        for row in table:
            anterior_id = row and row[0] or False
        anterior_id = anterior_id and anterior_id+1 or 1
        vals['anterior_id'] = anterior_id
        res_id = super(l10n_ec_hr_employee_family, self).create(cr, uid, vals, context=context)
        empleado = self.pool.get('hr.employee').browse(cr, uid, vals['employee_id'])
        if empleado.servicios_complementarios!=True:
            self._grabar_sqlserver(cr, uid, 'create', anterior_id, empleado.anterior_id, vals.copy())
        return res_id

    def write(self, cr, uid, ids, vals, context=None):
        res = super(l10n_ec_hr_employee_family, self).write(cr, uid, ids, vals, context=context)
        for this in self.browse(cr, uid, ids, context=context):
            self._grabar_sqlserver(cr, uid, 'write', this.anterior_id, this.employee_id.anterior_id, vals.copy())
        return res

    def unlink(self, cr, uid, ids, context=None):
        for this in self.browse(cr, uid, ids, context=context):
            self._grabar_sqlserver(cr, uid, 'unlink', this.anterior_id, this.employee_id.anterior_id, {})
        res = super(l10n_ec_hr_employee_family, self).unlink(cr, uid, ids, context=context)
        return res

l10n_ec_hr_employee_family()

class l10n_ec_hr_academic_level(osv.osv):
    _name = 'hr.academic.level'
    _description = 'Niveles Academicos'
    _order = 'name asc'
    _columns = dict(
        active = fields.boolean(u'Activo'),
        anterior_id = fields.integer(u'ID Anterior'),
        name = fields.char(u'Nivel', size=100, required=True),
        description = fields.char(u'Descripción', size=100),
        #status = fields.char(u'Status', size=2),
        type = fields.selection([('NINGUNA','NINGUNA'),('BASICO','BASICO'),('PRIMER NIVEL','PRIMER NIVEL'),('FORMACION SUPERIOR','FORMACION SUPERIOR'),('POSTGRADO','POSTGRADO')], u'Tipo'),
        )

    _defaults = {
        'active': True,
    }
l10n_ec_hr_academic_level()

class l10n_ec_hr_academic_area(osv.osv):
    _name = 'hr.academic.area'
    _description = 'Area Academica'
    _order = 'name asc'
    _columns = dict(
        active = fields.boolean(u'Activo'),
        anterior_id = fields.integer(u'ID Anterior'),
        name = fields.char(u'Area de conocimiento', size=100, required=True),
        description = fields.char(u'Descripción', size=100),
        #status = fields.char(u'Status', size=2),
        )

    _defaults = {
        'active': True,
    }
l10n_ec_hr_academic_area()

class l10n_ec_hr_employee_courses(osv.osv):
    _name = 'hr.employee.courses'
    _description = 'Cursos Empleado'
    _MODALITY = [('v',u'Virtual'),('d',u'Distancia'),('p',u'Presencial'),
                 ('s',u'Semipresencial'),('o',u'Otros')]
    _columns = dict(
        employee_id = fields.many2one('hr.employee', u'Empleado'),
        anterior_id = fields.integer(u'ID Anterior'),
        name = fields.char(u'Tema',size=128,required=True),
        date = fields.date(u'Fecha Inicio'),
        date_end = fields.date(u'Fecha Fin'),
        institute = fields.char(u'Institución',size=100),
        country_id = fields.many2one('res.country', u'País'),
        #city_id = fields.many2one('res.country.state.city', u'Ciudad'),
        city = fields.char(u'Ciudad', size=50),
        duration =  fields.integer(u'Duración'),
        type = fields.selection([(u'Certificación',u'Certificación'),(u'Curso',u'Curso'),(u'Seminario',u'Seminario')], u'Tipo de Curso'),
        area_id = fields.many2one('hr.academic.area', u'Area de conocimiento'),
        )

    def _grabar_sqlserver(self, cr, uid, tipo, id, empleado_id, valores):
        import pyodbc
        import sys
        sql_dict= {'employee_id': 'id_PERSO',
                   'name': 'TITULO',
                   'date': 'FECHA_INI',
                   'date_end': 'FECHA_FIN',
                   'institute': 'UNIVERSIDAD',
                   'country_id': 'ID_PAIS',
                   'pais': 'PAIS',
                   'city': 'CIUDAD',
                   'type': 'CURSO',
                   'area_id': 'ID_COMP',
                   'area_conoc': 'AREA_CONOC',
                   'duration': 'DURACION'}
        #PRIMERO REALIZAR LOS CAMBIOS
        if valores.has_key('employee_id'):
            dato = self.pool.get('hr.employee').browse(cr, uid, valores['employee_id'])
            valores['employee_id'] = dato.anterior_id
        else:
            valores['employee_id'] = empleado_id
        if valores.has_key('country_id'):
            dato = self.pool.get('res.country').browse(cr, uid, valores['country_id'])
            valores['country_id'] = dato.code_phone
            valores['pais'] = dato.name.upper()
        if valores.has_key('area_id'):
            dato = self.pool.get('hr.academic.area').browse(cr, uid, valores['area_id'])
            valores['area_id'] = dato.anterior_id
            valores['area_conoc'] = dato.name
        for key in valores.keys():
            #print str(type(valores[key])) + ": " + str(key) + " ; " + str(valores[key])
            if str(type(valores[key]))=="<type 'unicode'>":
                valores[key] = unicodedata.normalize('NFKD', valores[key]).encode('ascii','ignore')
                #print "modificado"
        #import pdb
        #pdb.set_trace()
        if tipo=='create':
            try:
                cnxn = pyodbc.connect('DSN=SQLS_LI;UID=odo;PWD=odo2233')
                cursor = cnxn.cursor()
                cursor.execute('insert into PERSO_CURSO (ID, ID_PERSO, CURSO, UNIVERSIDAD, TITULO, PAIS, CIUDAD, FECHA_INI, FECHA_FIN, DURACION, AREA_CONOC, ID_PAIS, ID_COMP) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (id, valores['employee_id'], str(valores['type']), valores['institute'], valores['name'], valores['pais'], valores['city'], valores['date'], valores['date_end'], valores['duration'], valores['area_conoc'], valores['country_id'], valores['area_id']))
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
                cursor.execute('update PERSO_CURSO SET ' + sql_dict[key] + '=? WHERE id=? and id_perso=?', (valores[key], id, valores['employee_id']))
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
                cursor.execute('delete from PERSO_CURSO WHERE id=? and id_perso=?', (id, valores['employee_id']))
                cnxn.commit()
                cnxn.close()
            except pyodbc.Error, err:
                raise osv.except_osv("Error!", err)
            except osv.except_osv, err:
                raise osv.except_osv("Error!", err)
            except:
                raise osv.except_osv("Error!", sys.exc_info()[0])

    def create(self, cr, uid, vals, context=None):
        cr.execute("select max(anterior_id) from hr_employee_courses where employee_id="+str(vals['employee_id']))
        table = cr.fetchall()
        anterior_id=False
        for row in table:
            anterior_id = row and row[0] or False
        anterior_id = anterior_id and anterior_id+1 or 1
        vals['anterior_id'] = anterior_id
        res_id = super(l10n_ec_hr_employee_courses, self).create(cr, uid, vals, context=context)
        empleado = self.pool.get('hr.employee').browse(cr, uid, vals['employee_id'])
        self._grabar_sqlserver(cr, uid, 'create', anterior_id, empleado.anterior_id, vals.copy())
        return res_id

    def write(self, cr, uid, ids, vals, context=None):
        res = super(l10n_ec_hr_employee_courses, self).write(cr, uid, ids, vals, context=context)
        for this in self.browse(cr, uid, ids, context=context):
            self._grabar_sqlserver(cr, uid, 'write', this.anterior_id, this.employee_id.anterior_id, vals.copy())
        return res

    def unlink(self, cr, uid, ids, context=None):
        for this in self.browse(cr, uid, ids, context=context):
            self._grabar_sqlserver(cr, uid, 'unlink', this.anterior_id, this.employee_id.anterior_id, {})
        res = super(l10n_ec_hr_employee_courses, self).unlink(cr, uid, ids, context=context)
        return res

l10n_ec_hr_employee_courses()

class l10n_ec_hr_employee_academic(osv.osv):   
    _name= 'hr.employee.academic'
    _description = 'Titulos Empleado'

    _columns = dict(
        employee_id = fields.many2one('hr.employee', u'Empleado'),
        anterior_id = fields.integer(u'ID Anterior'),
        name = fields.char(u'Título',size=100),
        institute = fields.char(u'Institución', size=100),
        country_id = fields.many2one('res.country', u'País'),
        date_start = fields.date(u'Fecha Inicio'),
        date_stop = fields.date(u'Fecha Finalización'),
        level_id = fields.many2one('hr.academic.level', u'Nivel'),
        area_id = fields.many2one('hr.academic.area', u'Area de conocimiento'),
        code = fields.char(u'Codigo SENESCYT', size=50),
        honores = fields.selection([('Si','Si'),('No','No')],u'Honores'),
        )

    def _grabar_sqlserver(self, cr, uid, tipo, id, empleado_id, valores):
        import pyodbc
        import sys
        sql_dict= {'employee_id': 'ID_PERSO',#
                   'name': 'TITULO', #
                   'date_start': 'FECHA_INI', #
                   'date_stop': 'FECHA_GRA',#
                   'institute': 'UNIVERSIDAD',#
                   'country_id': 'ID_PAIS',#
                   'pais': 'PAIS',#
                   'level_id': 'NIVEL',#
                   'area_id': 'ID_COMP',#
                   'honores': 'HONORES',#
                   'area_conoc': 'AREA_CONOC',}
        #PRIMERO REALIZAR LOS CAMBIOS
        if valores.has_key('employee_id'):
            dato = self.pool.get('hr.employee').browse(cr, uid, valores['employee_id'])
            valores['employee_id'] = dato.anterior_id
        else:
            valores['employee_id'] = empleado_id
        if valores.has_key('country_id'):
            dato = self.pool.get('res.country').browse(cr, uid, valores['country_id'])
            valores['country_id'] = dato.code_phone
            valores['pais'] = dato.name.upper()
        if valores.has_key('area_id'):
            dato = self.pool.get('hr.academic.area').browse(cr, uid, valores['area_id'])
            valores['area_id'] = dato.anterior_id
            valores['area_conoc'] = dato.name
        if valores.has_key('level_id'):
            dato = self.pool.get('hr.academic.level').browse(cr, uid, valores['level_id'])
            valores['level_id'] = dato.name
        for key in valores.keys():
            #print str(type(valores[key])) + ": " + str(key) + " ; " + str(valores[key])
            if str(type(valores[key]))=="<type 'unicode'>":
                valores[key] = unicodedata.normalize('NFKD', valores[key]).encode('ascii','ignore')
                #print "modificado"
        #import pdb
        #pdb.set_trace()
        if tipo=='create':
            try:
                cnxn = pyodbc.connect('DSN=SQLS_LI;UID=odo;PWD=odo2233')
                cursor = cnxn.cursor()
                cursor.execute('insert into PERSO_EDUCA (ID, ID_PERSO, UNIVERSIDAD, TITULO, PAIS, FECHA_INI, FECHA_GRA, AREA_CONOC, ID_PAIS, ID_COMP, NIVEL, HONORES) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (id, valores['employee_id'], valores['institute'], valores['name'], valores['pais'], valores['date_start'], valores['date_stop'],  valores['area_conoc'], valores['country_id'], valores['area_id'], valores['level_id'], valores['honores']))
                cnxn.commit()
                cnxn.close()
            except pyodbc.Error, err:
                raise osv.except_osv("Error!", err)
            except exceptions.KeyError, err:
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
                cursor.execute('update PERSO_EDUCA SET ' + sql_dict[key] + '=? WHERE id=? and id_perso=?', (valores[key], id, valores['employee_id']))
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
                cursor.execute('delete from PERSO_EDUCA WHERE id=? and id_perso=?', (id, valores['employee_id']))
                cnxn.commit()
                cnxn.close()
            except pyodbc.Error, err:
                raise osv.except_osv("Error!", err)
            except osv.except_osv, err:
                raise osv.except_osv("Error!", err)
            except:
                raise osv.except_osv("Error!", sys.exc_info()[0])

    def create(self, cr, uid, vals, context=None):
        cr.execute("select max(anterior_id) from hr_employee_academic where employee_id="+str(vals['employee_id']))
        table = cr.fetchall()
        anterior_id=False
        for row in table:
            anterior_id = row and row[0] or False
        anterior_id = anterior_id and anterior_id+1 or 1
        vals['anterior_id'] = anterior_id
        res_id = super(l10n_ec_hr_employee_academic, self).create(cr, uid, vals, context=context)
        empleado = self.pool.get('hr.employee').browse(cr, uid, vals['employee_id'])
        self._grabar_sqlserver(cr, uid, 'create', anterior_id, empleado.anterior_id, vals.copy())
        return res_id

    def write(self, cr, uid, ids, vals, context=None):
        res = super(l10n_ec_hr_employee_academic, self).write(cr, uid, ids, vals, context=context)
        for this in self.browse(cr, uid, ids, context=context):
            self._grabar_sqlserver(cr, uid, 'write', this.anterior_id, this.employee_id.anterior_id, vals.copy())
        return res

    def unlink(self, cr, uid, ids, context=None):
        for this in self.browse(cr, uid, ids, context=context):
            self._grabar_sqlserver(cr, uid, 'unlink', this.anterior_id, this.employee_id.anterior_id, {})
        res = super(l10n_ec_hr_employee_academic, self).unlink(cr, uid, ids, context=context)
        return res
    
l10n_ec_hr_employee_academic()


class l10n_ec_hr_employee(osv.osv):
    _inherit = 'hr.employee'

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
            name = ""
            if record.name_related:
                name = record.name_related
            res.append((record.id, name))
        return res
    
    def name_search(self, cr, uid, name='', args=[], operator='ilike', context={}, limit=80):
        ids = []
        ids_cedula = self.search(cr, uid, [('name', operator, name)] + args, limit=limit, context=context)
        ids = list(set(ids + ids_cedula))
        if name:
            ids_name = self.search(cr, uid, [('name_related', operator, name)] + args, limit=limit, context=context)
            ids = list(set(ids + ids_name))
        return self.name_get(cr, uid, ids, context=context)


    def _complete_name(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for employee in self.browse(cr, uid, ids):
            name = ""
            if employee.employee_lastname:
                name = name + employee.employee_lastname
            if employee.employee_name:
                name = name + " " + employee.employee_name
            res[employee.id] = name
        return res

    _BLOOD = [('on','O-'),('op','O+'),('an','A-'),('ap','A+'),
              ('bn','B-'),('bp','B+'),('abn','AB-'),('abp','AB+')]
    
    _columns = {
        #we need a related field in order to be able to sort the employee by name
        'name_related': fields.function(_complete_name, method=True, string=u"Nombre Completo", store=True, type="char", size=100),
        'employee_name': fields.char(u'Nombres', size=50, required=True),
        'employee_lastname': fields.char(u'Apellidos', size=50, required=True),
        'marital': fields.many2one('hr.marital.status',u'Estado Civil'),
        #'city_of_birth_id': fields.many2one('res.country.state.city',u'Ciudad de Nacimiento'),
        'place_of_birth': fields.many2one('res.country.state.city',u'Ciudad de Nacimiento'),
        'id_type': fields.selection([('c','Cedula'),('p','Pasaporte')], u"Tipo identificador", help=u"Tipo de identificador personal"),
        'blood_type':  fields.selection(_BLOOD,u'Tipo de sangre'),
        'disabled': fields.boolean(u'Es discapacitado?', help=u"Marque este campo si el empleado tiene alguna limitación para llevar a cabo ciertas actividades provocadas por una deficiencia física o mental"),
        'disability_id': fields.many2one('hr.employee.disability',u'Tipo de discapacidad'),
        'disability_percent': fields.float(u'Porcentaje de discapacidad'),
        'id_disability': fields.char(u'ID CONADIS', size=15, help=u"Codigo de identificación del CONADIS"),
        'emergency_contact': fields.char(u'Nombre del contacto', size=100, help=u"Indique el nombre y la relación del empleado con el contacto de emergencia"),
        'emergency_phone': fields.char(u'Telefono de contacto', size=30),
        'family_lines': fields.one2many('hr.employee.family', 'employee_id', u'Familares'),
        'projection_lines': fields.one2many('hr.employee.projection','employee_id',u'Proyección de Gastos personales'),
        'profit_lines': fields.one2many('hr.employee.profit','employee_id',u'Detalle rentabilidad'),
        'reference_lines': fields.one2many('hr.employee.reference','employee_id',u'Referencias Personales'),
        #'department_id': fields.related('job_id','department_id', type='many2one', relation='hr.department', string=u"Departmento", readonly=True, store=True),
        'academic_ids': fields.one2many('hr.employee.academic','employee_id',u'Formación Académica'),
        'courses_ids': fields.one2many('hr.employee.courses','employee_id',u'Cursos y Capacitaciones'),
        'personal_email': fields.char(u'E-mail Personal', size=240),
        'military_card': fields.char(u'Libreta Militar', size=30),
        #'occupational_code': fields.char(u'Código Ocupacional', size=30),
        'anterior_id': fields.integer(u'ID Anterior'),
        'medic_exam': fields.boolean(u'Exámen Médico'),
        'medic_exam_notes': fields.text(u'Observaciones de Exámen'),
        'servicios_complementarios': fields.boolean(u'Empleado Servicios Complementarios'),
        'retencion_judicial': fields.float(u'Retenciones Judiciales'),
        'experience_lines': fields.one2many('hr.employee.experience','employee_id',u'Experiencia Laboral'),
        'work_extension': fields.char(u'Extensión del Trabajo', size=10),
        'address_home_id': fields.char(u'Dirección Domicilio', size=200),
        'address_home_n': fields.char(u'Número Domicilio', size=10),
        'home_phone': fields.char(u'Teléfono Domicilio', size=10),
        'personal_mobile': fields.char(u'Celular', size=10),
        'bank_id': fields.many2one('res.bank', u'Banco'),
        'bank_account_type': fields.many2one('res.partner.bank.type', u'Tipo de Cuenta'),
        'bank_account_id': fields.char(u'Número de Cuenta', size=15),
    }

    _order='name_related'

    _defaults = {
        'servicios_complementarios': False,
        'retencion_judicial': 0.00,
        'company_id': False,
        'active': True,
    }

    def _grabar_sqlserver(self, cr, uid, tipo, id, valores):
        import pyodbc
        import sys
        sql_dict= {'active': 'STATUS', 'department_id': 'ID_AREA', 'job_id': 'ID_PSTO', 'birthday': 'FECHA_NACIMIENTO', 'gender': 'SEXO', 'marital': 'ESTADO_CIVIL', 'country_id':'PA_COD', 'nombre': 'NOMBRE'}
        sql_dict_ext= {'address_home_id': 'EP_DIRECCION', 'emergency_phone': 'EP_DIR_NUM', 'name': 'EP_CEDULA', 'id_type': 'EP_TIPO_CED', 'home_phone': 'EP_TELEFONO', 'ssnid': 'EP_NUM_SEGURO', 'nacionalidad': 'EP_NACIONALIDAD', 'personal_mobile': 'EP_TEL_MOVIL', 'paterno': 'EP_APELL_PATE', 'materno': 'EP_APELL_MAT', 'employee_name': 'EP_NOMBRES', 'personal_email': 'EP_MAIL', 'blood_type': 'EP_TIPOSANGRE'}
        #PRIMERO REALIZAR LOS CAMBIOS
        if valores.has_key('active'):
            valores['active'] = valores['active']==True and 'A' or 'E'
        if valores.has_key('department_id'):
            dato = self.pool.get('hr.department').browse(cr, uid, valores['department_id'])
            valores['department_id'] = dato.anterior_id
        if valores.has_key('job_id'):
            dato = self.pool.get('hr.job').browse(cr, uid, valores['job_id'])
            valores['job_id'] = dato.anterior_id
        if valores.has_key('marital'):
            dato = self.pool.get('hr.marital.status').browse(cr, uid, valores['marital'])
            valores['marital'] = dato.name
        if valores.has_key('country_id'):
            dato = self.pool.get('res.country').browse(cr, uid, valores['country_id'])
            valores['country_id'] = dato.code_phone
            valores['nacionalidad'] = dato.name
        #if valores.has_key('address_home_id'):
        #    dato = self.pool.get('res.partner').browse(cr, uid, valores['address_home_id'])
        #    valores['address_home_id'] = dato.street
        #    valores['telefono'] = dato.phone
        #    valores['celular'] = dato.mobile
        #if valores.has_key('blood_type'):
        #    dato = self.pool.get('res.partner').browse(cr, uid, valores['address_home_id'])
        #    valores['address_home_id'] = dato.street
        #    valores['telefono'] = dato.phone
        #    valores['celular'] = dato.mobile
        if valores.has_key('employee_lastname') or valores.has_key('employee_name'):
            #import pdb
            #pdb.set_trace()
            dato_id = self.pool.get('hr.employee').search(cr, uid, [('anterior_id','=',id)])
            if dato_id:
                valores['nombre'] = self.pool.get('hr.employee').browse(cr, uid, dato_id[0]).name_related
        if valores.has_key('employee_lastname'):
            valores['paterno'] = valores['employee_lastname'].split(' ')[0]
            valores['materno'] = valores['employee_lastname'].split(' ')[1] and valores['employee_lastname'].split(' ')[1] or ''
        if valores.has_key('gender'):
            valores['gender'] = valores['gender'][:1].upper()
        if valores.has_key('blood_type'):
          if valores['blood_type']:
            BLOOD = {'on':'O-','op':'O+','an':'A-','ap':'A+','bn':'B-','bp':'B+','abn':'AB-','abp':'AB+'}
            valores['blood_type'] = BLOOD[valores['blood_type']]
        if valores.has_key('id_type'):
            valores['id_type'] = valores['id_type'].upper()
        #import pdb
        #pdb.set_trace()
        for key in valores.keys():
            if str(type(valores[key]))=="<type 'unicode'>":
                valores[key] = unicodedata.normalize('NFKD', valores[key]).encode('ascii','ignore')
        if tipo=='create':
            try:
                cnxn = pyodbc.connect('DSN=SQLS_LI;UID=odo;PWD=odo2233')
                cursor = cnxn.cursor()
                cursor.execute("""insert into PERSONAS (ID,
                                                        ID_AREA,
                                                        ID_PSTO,
                                                        ID_SPRV,
                                                        NOMBRE,
                                                        COD_INT,
                                                        FECHA_INGRESO,
                                                        FECHA_NACIMIENTO,
                                                        SEXO,
                                                        SUELDO_BASICO,
                                                        ESTADO_CIVIL,
                                                        CARGAS,
                                                        STATUS,
                                                        ID_SPRV2,
                                                        POTENCIAL,
                                                        PA_COD,
                                                        PA_CIU_COD,
                                                        DIS_ID,
                                                        LOCALIDAD) VALUES (?,
                                                                           ?,
                                                                           ?,
                                                                           NULL,
                                                                           ?,
                                                                           0.00,
                                                                           ?,
                                                                           ?,
                                                                           ?,
                                                                           0.00,
                                                                           ?,
                                                                           ?,
                                                                           ?,
                                                                           NULL,
                                                                           0,
                                                                           ?,
                                                                           ?,
                                                                           1,
                                                                           '')""", #LOCALIDAD ES LA CIUDAD DEL CONTRATO
                               (id,
                                valores.has_key('department_id') and valores['department_id'] or False,
                                valores.has_key('job_id') and valores['job_id'] or False,
                                valores['employee_lastname'] + ' ' + valores['employee_name'],
                                strftime("%Y-%m-%d"),
                                valores['birthday'],
                                valores['gender'],
                                valores['marital'],
                                valores.has_key('family_lines') and len(valores['family_lines']) or 0,
                                valores['active'],
                                valores.has_key('country_id') and valores['country_id'] or '',
                                '' ))
                #cnxn.commit()
                #import pdb
                #pdb.set_trace()
                cursor.execute("""INSERT INTO EXT_PERSONA (ID,
                                                           BA_BAN_ID,
                                                           CB_CUENTA_ID,
                                                           REG_COD,
                                                           PR_COD,
                                                           CA_COD,
                                                           CIU_COD,
                                                           SUC_COD,
                                                           EP_DIRECCION,
                                                           EP_CEDULA,
                                                           EP_TIPO_CED,
                                                           EP_TELEFONO,
                                                           EP_FECHA_SALIDA,
                                                           EP_NUM_SEGURO,
                                                           EP_TIPO_CONTRATO,
                                                           EP_NACIONALIDAD,
                                                           EP_DIR_NUM,
                                                           EP_TEL_MOVIL,
                                                           EP_FORMA_PAGO,
                                                           EP_APELL_PATE,
                                                           EP_APELL_MAT,
                                                           EP_NOMBRES,
                                                           EP_MAIL,
                                                           EP_TIPO_EMP,
                                                           EP_SERVICIO,
                                                           EP_APORTA,
                                                           EP_CATEGOR,
                                                           EP_FOTO,
                                                           EP_TIPOSANGRE) VALUES (?,
                                                                                   0,
                                                                                   0,
                                                                                   '0',
                                                                                   '0',
                                                                                   '0',
                                                                                   '0',
                                                                                   1,
                                                                                   ?,
                                                                                   ?,
                                                                                   ?,
                                                                                   ?,
                                                                                   '',
                                                                                   ?,
                                                                                   ?,
                                                                                   ?,
                                                                                   ?,
                                                                                   ?,
                                                                                   ?,
                                                                                   ?,
                                                                                   ?,
                                                                                   ?,
                                                                                   ?,
                                                                                   '',
                                                                                   'NO',
                                                                                   'NO',
                                                                                   '0',
                                                                                   'EJEMPLO.JPG',
                                                                                   ?)""",
                               (id,
                                valores['address_home_id'],
                                valores['name'],
                                valores['id_type'],
                                valores['home_phone'], #luego de esta va ep_fecha_salida
                                valores.has_key('ssnid') and valores['ssnid'] or '',
                                'FIJO',
                                valores.has_key('nacionalidad') and valores['nacionalidad'] or '',
                                valores.has_key('emergency_phone') and valores['emergency_phone'] or '',
                                valores['personal_mobile'],
                                valores.has_key('bank_account_id') and 'B' or 'E',
                                valores['paterno'],
                                valores['materno'],
                                valores['employee_name'],
                                valores.has_key('personal_email') and valores['personal_email'] or '',
                                valores['blood_type'],))
                cnxn.commit()
                cnxn.close()
            except pyodbc.Error, err:
                raise osv.except_osv("Error!", err)
            except osv.except_osv, err:
                raise osv.except_osv("Error!", err)
            except exceptions.KeyError, err:
                raise osv.except_osv("Error!", err)
            except exceptions.UnicodeEncodeError, err:
                raise osv.except_osv("Error!", err)
            except:
                raise osv.except_osv("Error!", sys.exc_info()[0])
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
        if tipo=='unlink':
            try:
                cnxn = pyodbc.connect('DSN=SQLS_LI;UID=odo;PWD=odo2233')
                cursor = cnxn.cursor()
                cursor.execute('delete from EXT_PERSONA WHERE id=?', (id))
                cursor.execute('delete from PERSONAS WHERE id=?', (id))
                cnxn.commit()
                cnxn.close()
            except pyodbc.Error, err:
                raise osv.except_osv("Error!", err)
            except osv.except_osv, err:
                raise osv.except_osv("Error!", err)
            except:
                raise osv.except_osv("Error!", sys.exc_info()[0])

    def create(self, cr, uid, vals, context=None):
        anterior_id=False
        if not(vals.has_key('servicios_complementarios')) or vals['servicios_complementarios']==False:
                cr.execute("select max(anterior_id) from hr_employee")
                table = cr.fetchall()
                for row in table:
                    anterior_id = row and row[0] or False
                anterior_id = anterior_id and anterior_id+1 or 1
                vals['anterior_id'] = anterior_id
        res_id = super(l10n_ec_hr_employee, self).create(cr, uid, vals, context=context)
        if not(vals.has_key('servicios_complementarios')) or vals['servicios_complementarios']==False:
                self._grabar_sqlserver(cr, uid, 'create', anterior_id, vals.copy())
        return res_id

    def write(self, cr, uid, ids, vals, context=None):
        res = super(l10n_ec_hr_employee, self).write(cr, uid, ids, vals, context=context)
        for this in self.browse(cr, uid, ids, context=context):
          if this.servicios_complementarios==False:
            self._grabar_sqlserver(cr, uid, 'write', this.anterior_id, vals.copy())
        return res

    def unlink(self, cr, uid, ids, context=None):
        raise osv.except_osv(u"Error!", u"No puede eliminar un empleado del sistema. Desactive o reutilice el registro.")
        return False
        """for this in self.browse(cr, uid, ids, context=context):
          if this.servicios_complementarios==False:
            self._grabar_sqlserver(cr, uid, 'unlink', this.anterior_id, {})
        res = super(l10n_ec_hr_employee, self).unlink(cr, uid, ids, context=context)
        return res"""

    def _check_identificador(self, cr, uid, ids):
        from openerp.addons.l10n_ec_tools import functions
        for employee in self.browse(cr, uid, ids):
            if employee.id_type=='c':
                return functions._check_cedula(employee.name)
            else:
                return True

    def _check_duplication(self, cr, uid, ids):
        for employee in self.browse(cr, uid, ids):
            empleados = self.search(cr, uid, [('id_type','=',employee.id_type),('name','=',employee.name)])
            if len(empleados)>1:
                return False
            else:
                return True

    _constraints = [
        (_check_identificador, u'El identificador es inválido, por favor verifique', ['name']),
        (_check_duplication, u'El registro es inválido, no se puede repetir empleados con el mismo identificador', ['id_type','name']),
        ]


l10n_ec_hr_employee()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
