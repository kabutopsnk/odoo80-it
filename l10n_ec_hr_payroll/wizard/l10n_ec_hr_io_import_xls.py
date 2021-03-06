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


from openerp.osv import osv,fields
import base64
import xlrd

class l10n_ec_hr_io_head_import(osv.osv_memory):

    _name='wizard.import.hr.io.head'
    _description='Asistente para importar ingresos/egresos desde XLS'
    
    _columns={'archivo':fields.binary('Archivo', required=True)}

    def _bad_archivo(self, cr, uid, ids, arch,context=None):
        result = True
        emp_obj = self.pool.get('hr.employee')
        arch_xls = base64.b64decode(arch)
        book = xlrd.open_workbook(file_contents=arch_xls)
        sh = book.sheet_by_name(book.sheet_names()[0])
        j=i=0
        for r in range(sh.nrows)[1:]:
            i+=1
            if sh.cell(r,0).value and sh.cell(r,1).value and sh.cell(r,2).value:
                emp_id = emp_obj.search(cr, uid, [('name','=',sh.cell(r,1).value)])
                if emp_id:
                    j+=1
                else:
                    raise osv.except_osv(('Error de archivo!'),'La cedula %s, en la linea numero %d no corresponde a ningun empleado'%((str(sh.cell(r,1).value)),i+1))
            else:
                raise osv.except_osv(('Error de archivo!'),'Existe un campo que esta vacio en la linea %s '%(r))
        if j==sh.nrows:
            result = True
        return result

    def import_sheet(self, cr, uid, ids, context={}):
        emp_obj = self.pool.get('hr.employee')
        data = self.read(cr, uid, ids)[0]
        line_obj = self.pool.get('hr.io.line')
        self._bad_archivo(cr, uid, ids, data['archivo'], context=context)
        obj = self.pool.get('hr.io.head')
        id_activo = context.get('active_id')
        parent = obj.browse(cr, uid, id_activo)
        ids_unlink=[]
        if parent.state != 'draft':
            raise osv.except_osv(('Error de usuario!'),'No puede importar un archivo cuando el documento ya esta procesado.')
        for l in parent.line_ids:
            if l.state=='draft':
                ids_unlink.append(l.id)
        line_obj.unlink(cr, uid, ids_unlink, context=context)
        if data['archivo']:
            arch = data['archivo']
            arch_xls = base64.b64decode(arch)
            book = xlrd.open_workbook(file_contents=arch_xls)
            sh = book.sheet_by_name(book.sheet_names()[0])
            context={}
            for r in range(sh.nrows)[1:]:
                if sh.cell(r,0).value and sh.cell(r,1).value and sh.cell(r,2).value:
                    emp_id = emp_obj.search(cr, uid, [('name','=',sh.cell(r,1).value)])
                    if emp_id:
                        for emp in emp_id:
                            empleado=emp_obj.browse(cr, uid, emp)
                            line_obj.create(cr, uid, {
                                                      'employee_id':empleado.id,
                                                      'value':sh.cell(r,2).value,
                                                      'rule_id':parent.rule_id.id,
                                                      'head_id':parent.id,
                                                      'date':parent.date,
                                                      'biweekly':parent.biweekly,
                                                      'label': sh.cell(r,3).value and sh.cell(r,3).value or '',
                                                      })
        else:
            raise osv.except_osv(('Error de usuario!'),'No ha seleccionado ningun archivo.')
        return {'type':'ir.actions.act_window_close' }

l10n_ec_hr_io_head_import()


