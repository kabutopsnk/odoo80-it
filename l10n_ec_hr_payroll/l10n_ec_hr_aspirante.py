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


class l10n_ec_hr_aspirante(osv.osv):
    _name = 'hr.aspirante'

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
    
    _columns = {
        #we need a related field in order to be able to sort the employee by name
        'id_type': fields.selection([('c','Cedula'),('p','Pasaporte')], u"Tipo identificador", help=u"Tipo de identificador personal", required=True),
        'name': fields.char(u'Identificador', size=20, required=True),
        'name_related': fields.function(_complete_name, method=True, string=u"Nombre Completo", store=True, type="char", size=100),
        'employee_name': fields.char(u'Nombres', size=50, required=True),
        'employee_lastname': fields.char(u'Apellidos', size=50, required=True),
        'personal_mobile': fields.char(u'Celular', size=10),
        'personal_email': fields.char(u'E-mail Personal', size=240),
        'address_home_id': fields.char(u'Dirección Domicilio', size=200),
        'address_home_n': fields.char(u'Número Domicilio', size=10),
        'home_phone': fields.char(u'Teléfono Domicilio', size=10),
        'marital': fields.many2one('hr.marital.status',u'Estado Civil'),
        'reference_lines': fields.one2many('hr.aspirante.reference','aspirante_id',u'Referencias Personales'),
        'academic_ids': fields.one2many('hr.aspirante.academic','aspirante_id',u'Formación Académica'),
        'courses_ids': fields.one2many('hr.aspirante.courses','aspirante_id',u'Cursos y Capacitaciones'),
        'experience_lines': fields.one2many('hr.aspirante.experience','aspirante_id',u'Experiencia Laboral'),
        'resultados': fields.one2many('hr.aspirante.resultado','aspirante_id',u'Resultados'),
        'state': fields.selection([('aspirante','Aspirante'),('empleado','Empleado')], string=u"Estado", required=True),
    }
    
    defaults = {
        'state':'aspirante'
    }

    _order='name_related'


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
        (_check_duplication, u'El registro es inválido, no se puede repetir aspirantes con el mismo identificador', ['id_type','name']),
        ]

l10n_ec_hr_aspirante()


class l10n_ec_hr_aspirante_reference(osv.osv):
    _name = 'hr.aspirante.reference'
    _description = 'Referencias personales de un Aspirante'
    _order = 'name desc'

    _columns = {
        'aspirante_id':  fields.many2one('hr.aspirante', u'Aspirante', ondelete='cascade'),
        'name': fields.char(u'Nombre', size=50, required=True),
        'phone': fields.char(u'Teléfono', size=30, required=True),
        'email': fields.char(u'Email', size=50),
    }

l10n_ec_hr_aspirante_reference()

class l10n_ec_hr_aspirante_academic(osv.osv):   
    _name= 'hr.aspirante.academic'
    _description = 'Titulos Aspirante'

    _columns = dict(
        aspirante_id = fields.many2one('hr.aspirante', u'Aspirante', ondelete='cascade'),
        #anterior_id = fields.integer(u'ID Anterior'),
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
    
l10n_ec_hr_aspirante_academic()

class l10n_ec_hr_aspirante_courses(osv.osv):
    _name = 'hr.aspirante.courses'
    _description = 'Cursos Aspirante'
    _MODALITY = [('v',u'Virtual'),('d',u'Distancia'),('p',u'Presencial'),
                 ('s',u'Semipresencial'),('o',u'Otros')]
    _columns = dict(
        aspirante_id = fields.many2one('hr.aspirante', u'Aspirante', ondelete='cascade'),
        #anterior_id = fields.integer(u'ID Anterior'),
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

l10n_ec_hr_aspirante_courses()

class ec_hr_aspirante_experience(osv.osv):
    _name = 'hr.aspirante.experience'
    _description = 'Experiencia Laboral de un Aspirante'

    _columns = {
        'aspirante_id':  fields.many2one('hr.aspirante', u'Aspirante', ondelete='cascade'),
        #'anterior_id': fields.integer(u'ID Anterior'),
        'institution': fields.char(u'Institución', size=100),
        'job': fields.char(u'Cargo', size=100),
        'sector_id': fields.many2one('hr.aspirante.experience.sector', u'Sector'),
        'date_start': fields.date(u'Fecha de ingreso'),
        'date_stop': fields.date(u'Fecha de salida'),
        'experience_institution_id': fields.many2one('hr.aspirante.experience.institution', u'Experiencia en instituciones de tipo'),
        'experience_job_id': fields.many2one('hr.aspirante.experience.job', u'Experiencia en cargos de tipo'),
        'description': fields.char(u'Descripción', size=200),
        'reference_name': fields.char(u'Nombre de la ref.', size=100),
        'reference_institution': fields.char(u'Institución de ref.', size=100),
        'reference_job': fields.char(u'Cargo de la ref.', size=100),
        'reference_phone': fields.char(u'Teléfono de la ref.', size=30),
    }

ec_hr_aspirante_experience()

class hr_aspirante_resultado(osv.osv):
    _name = 'hr.aspirante.resultado'
    _description = 'Resultados de aspirante'
    _order = 'name desc'

    _columns = {
        'aspirante_id':  fields.many2one('hr.aspirante', u'Aspirante', ondelete='cascade'),
        'name': fields.char(u'Descripcion', size=50, required=True),
        'check': fields.selection([('yes','SI'),('no','NO')], u'SI/NO', required=True),
        'notes': fields.text(u'Observaciones'),
    }

hr_aspirante_resultado()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
