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
#    but WITHOUT ANY WARRANTY; without_a even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv
from datetime import datetime
from time import strftime
import StringIO
import base64

class hr_italiana_bancos(osv.osv_memory):
    _name='hr.italiana.bancos'
    _description='Exportar archivo de rol a Bancos'

    _columns = {
                'datas_a0':fields.binary('ITALIMENTOS - Sin Banco'),
                'datas_a0_fname':fields.char('ITALIMENTOS - Nombre sin Banco', size=100),
                'datas_a1':fields.binary('ITALIMENTOS - Banco del Pichincha'),
                'datas_a1_fname':fields.char('ITALIMENTOS - Nombre Banco Pichincha', size=100),
                'datas_a2':fields.binary('ITALIMENTOS - Banco Internacional'),
                'datas_a2_fname':fields.char('ITALIMENTOS - Nombre Banco Internacional', size=100),
                'datas_a3':fields.binary('ITALIMENTOS - Banco del Austro'),
                'datas_a3_fname':fields.char('ITALIMENTOS - Nombre Banco Austro', size=100),

                'datas_b0':fields.binary('ITALDELI - Sin Banco'),
                'datas_b0_fname':fields.char('ITALDELI - Nombre sin Banco', size=100),
                'datas_b1':fields.binary('ITALDELI - Banco del Pichincha'),
                'datas_b1_fname':fields.char('ITALDELI - Nombre Banco Pichincha', size=100),
                'datas_b2':fields.binary('ITALDELI - Banco Internacional'),
                'datas_b2_fname':fields.char('ITALDELI - Nombre Banco Internacional', size=100),
                'datas_b3':fields.binary('ITALDELI - Banco del Austro'),
                'datas_b3_fname':fields.char('ITALDELI - Nombre Banco Austro', size=100),
                
                'datas_c0':fields.binary('VISEMSA - Sin Banco'),
                'datas_c0_fname':fields.char('VISEMSA - Nombre sin Banco', size=100),
                'datas_c1':fields.binary('VISEMSA - Banco del Pichincha'),
                'datas_c1_fname':fields.char('VISEMSA - Nombre Banco Pichincha', size=100),
                'datas_c2':fields.binary('VISEMSA - Banco Internacional'),
                'datas_c2_fname':fields.char('VISEMSA - Nombre Banco Internacional', size=100),
                'datas_c3':fields.binary('VISEMSA - Banco del Austro'),
                'datas_c3_fname':fields.char('VISEMSA - Nombre Banco Austro', size=100),

                'payroll_id': fields.many2one('hr.payslip.run','Rol'),
                }
    
    def rol_padre(self, cr, uid, context={}):
        return context.get('active_id')
    
    _defaults = {
                 'payroll_id': rol_padre,
                 }

    def generar_archivo(self, cr, uid, ids, context={}):
        for registro in self.browse(cr, uid, ids, context):
          buf_a0 = StringIO.StringIO()
          buf_a1 = StringIO.StringIO()
          buf_a2 = StringIO.StringIO()
          buf_a3 = StringIO.StringIO()
          buf_b0 = StringIO.StringIO()
          buf_b1 = StringIO.StringIO()
          buf_b2 = StringIO.StringIO()
          buf_b3 = StringIO.StringIO()
          buf_c0 = StringIO.StringIO()
          buf_c1 = StringIO.StringIO()
          buf_c2 = StringIO.StringIO()
          buf_c3 = StringIO.StringIO()
          for rol_individual in registro.payroll_id.slip_ids:
            if rol_individual.company_id.id==1 and not(rol_individual.employee_id.bank_id and rol_individual.employee_id.bank_account_type and rol_individual.employee_id.bank_account_id):
              #if rol_individual.employee_id.bank_id.bic=='00001':
                for rubro in rol_individual.line_ids:
                  if rubro.category_id.code=='NET':
                    #DETALLE DE LA LINEA
                    detalle = ''
                    detalle += '\t' + rol_individual.employee_id.name
                    detalle += '\t' + rol_individual.employee_id.name_related
                    detalle += '\t' + str(rubro.total)
                    detalle += '\t' + (rol_individual.employee_id.bank_id and rol_individual.employee_id.bank_id.bic or '')
                    detalle += '\t' + (rol_individual.employee_id.bank_id and rol_individual.employee_id.bank_id.name or '')
                    detalle += '\n'
                    detalle = detalle.encode('utf-8')
                    buf_a0.write(detalle.upper())
            if rol_individual.company_id.id==3 and not(rol_individual.employee_id.bank_id and rol_individual.employee_id.bank_account_type and rol_individual.employee_id.bank_account_id):
              #if rol_individual.employee_id.bank_id.bic=='00001':
                for rubro in rol_individual.line_ids:
                  if rubro.category_id.code=='NET':
                    #DETALLE DE LA LINEA
                    detalle = ''
                    detalle += '\t' + rol_individual.employee_id.name
                    detalle += '\t' + rol_individual.employee_id.name_related
                    detalle += '\t' + str(rubro.total)
                    detalle += '\t' + (rol_individual.employee_id.bank_id and rol_individual.employee_id.bank_id.bic or '')
                    detalle += '\t' + (rol_individual.employee_id.bank_id and rol_individual.employee_id.bank_id.name or '')
                    detalle += '\n'
                    detalle = detalle.encode('utf-8')
                    buf_b0.write(detalle.upper())
            if rol_individual.company_id.id==4 and not(rol_individual.employee_id.bank_id and rol_individual.employee_id.bank_account_type and rol_individual.employee_id.bank_account_id):
              #if rol_individual.employee_id.bank_id.bic=='00001':
                for rubro in rol_individual.line_ids:
                  if rubro.category_id.code=='NET':
                    #DETALLE DE LA LINEA
                    detalle = ''
                    detalle += '\t' + rol_individual.employee_id.name
                    detalle += '\t' + rol_individual.employee_id.name_related
                    detalle += '\t' + str(rubro.total)
                    detalle += '\t' + (rol_individual.employee_id.bank_id and rol_individual.employee_id.bank_id.bic or '')
                    detalle += '\t' + (rol_individual.employee_id.bank_id and rol_individual.employee_id.bank_id.name or '')
                    detalle += '\n'
                    detalle = detalle.encode('utf-8')
                    buf_c0.write(detalle.upper())
            if rol_individual.company_id.id==1 and rol_individual.employee_id.bank_id and rol_individual.employee_id.bank_account_type and rol_individual.employee_id.bank_account_id:
              if rol_individual.employee_id.bank_id.bic=='00001':
                for rubro in rol_individual.line_ids:
                  if rubro.category_id.code=='NET' and rubro.total>0:
                    monto=rubro.total
                    monto_str=(("%.2f"%monto).replace(".",'')).rjust(13,'0')
                    #DETALLE DE LA LINEA
                    detalle = 'PA'
                    detalle += '\t' + str(rol_individual.employee_id.anterior_id).rjust(5,'0')
                    detalle += '\t' + 'USD'
                    detalle += '\t' + monto_str
                    detalle += '\t' + 'CTA'
                    detalle += '\t' + rol_individual.employee_id.bank_account_type.code
                    detalle += '\t' + rol_individual.employee_id.bank_account_id
                    detalle += '\t' + registro.payroll_id.name
                    detalle += '\t' + 'C'
                    detalle += '\t' + rol_individual.employee_id.name
                    detalle += '\t' + rol_individual.employee_id.name_related
                    detalle += '\n'
                    detalle = detalle.encode('utf-8')
                    buf_a1.write(detalle.upper())
                  if rubro.category_id.code=='NET' and rubro.total<=0:
                    #DETALLE DE LA LINEA
                    detalle = ''
                    detalle += '\t' + rol_individual.employee_id.name
                    detalle += '\t' + rol_individual.employee_id.name_related
                    detalle += '\t' + str(rubro.total)
                    detalle += '\t' + (rol_individual.employee_id.bank_id and rol_individual.employee_id.bank_id.bic or '')
                    detalle += '\t' + (rol_individual.employee_id.bank_id and rol_individual.employee_id.bank_id.name or '')
                    detalle += '\n'
                    detalle = detalle.encode('utf-8')
                    buf_a0.write(detalle.upper())
              if rol_individual.employee_id.bank_id.bic=='00002':
                for rubro in rol_individual.line_ids:
                  if rubro.category_id.code=='NET' and rubro.total>0:
                    monto=rubro.total
                    monto_str=(("%.2f"%monto).replace(".",'')).rjust(13,'0')
                    #DETALLE DE LA LINEA
                    detalle = 'PA'
                    detalle += '\t' + registro.payroll_id.name[:20]
                    detalle += '\t' + 'USD'
                    detalle += '\t' + monto_str
                    detalle += '\t' + 'CTA'
                    detalle += '\t' + rol_individual.employee_id.bank_account_type.code
                    detalle += '\t' + rol_individual.employee_id.bank_account_id
                    detalle += '\t' + registro.payroll_id.name
                    detalle += '\t' + 'C'
                    detalle += '\t' + rol_individual.employee_id.name
                    detalle += '\t' + rol_individual.employee_id.name_related
                    detalle += '\t' + '32'
                    detalle += '\n'
                    detalle = detalle.encode('utf-8')
                    buf_a2.write(detalle.upper())
                  if rubro.category_id.code=='NET' and rubro.total<=0:
                    #DETALLE DE LA LINEA
                    detalle = ''
                    detalle += '\t' + rol_individual.employee_id.name
                    detalle += '\t' + rol_individual.employee_id.name_related
                    detalle += '\t' + str(rubro.total)
                    detalle += '\t' + (rol_individual.employee_id.bank_id and rol_individual.employee_id.bank_id.bic or '')
                    detalle += '\t' + (rol_individual.employee_id.bank_id and rol_individual.employee_id.bank_id.name or '')
                    detalle += '\n'
                    detalle = detalle.encode('utf-8')
                    buf_a0.write(detalle.upper())
              if rol_individual.employee_id.bank_id.bic=='00003':
                for rubro in rol_individual.line_ids:
                  if rubro.category_id.code=='NET' and rubro.total>0:
                    monto=rubro.total
                    monto_str=(("%.2f"%monto).replace(".",'')).rjust(13,'0')
                    #DETALLE DE LA LINEA
                    detalle = 'PA'
                    detalle += '\t' + 'C'
                    detalle += '\t' + rol_individual.employee_id.name
                    detalle += '\t' + rol_individual.employee_id.name
                    detalle += '\t' + rol_individual.employee_id.name_related
                    detalle += '\t' + rol_individual.employee_id.bank_account_type.code
                    detalle += '\t' + rol_individual.employee_id.bank_account_id
                    detalle += '\t' + 'USD'
                    detalle += '\t' + monto_str
                    detalle += '\t' + '0035'
                    detalle += '\n'
                    detalle = detalle.encode('utf-8')
                    buf_a3.write(detalle.upper())
                  if rubro.category_id.code=='NET' and rubro.total<=0:
                    #DETALLE DE LA LINEA
                    detalle = ''
                    detalle += '\t' + rol_individual.employee_id.name
                    detalle += '\t' + rol_individual.employee_id.name_related
                    detalle += '\t' + str(rubro.total)
                    detalle += '\t' + (rol_individual.employee_id.bank_id and rol_individual.employee_id.bank_id.bic or '')
                    detalle += '\t' + (rol_individual.employee_id.bank_id and rol_individual.employee_id.bank_id.name or '')
                    detalle += '\n'
                    detalle = detalle.encode('utf-8')
                    buf_a0.write(detalle.upper())
              if rol_individual.employee_id.bank_id.bic not in ('00001','00002','00003'):
                for rubro in rol_individual.line_ids:
                  if rubro.category_id.code=='NET':
                    detalle = ''
                    detalle += '\t' + rol_individual.employee_id.name
                    detalle += '\t' + rol_individual.employee_id.name_related
                    detalle += '\t' + str(rubro.total)
                    detalle += '\t' + (rol_individual.employee_id.bank_id and rol_individual.employee_id.bank_id.bic or '')
                    detalle += '\t' + (rol_individual.employee_id.bank_id and rol_individual.employee_id.bank_id.name or '')
                    detalle += '\n'
                    detalle = detalle.encode('utf-8')
                    buf_a0.write(detalle.upper())
            if rol_individual.company_id.id==3 and rol_individual.employee_id.bank_id and rol_individual.employee_id.bank_account_type and rol_individual.employee_id.bank_account_id:
              if rol_individual.employee_id.bank_id.bic=='00001':
                for rubro in rol_individual.line_ids:
                  if rubro.category_id.code=='NET' and rubro.total>0:
                    monto=rubro.total
                    monto_str=(("%.2f"%monto).replace(".",'')).rjust(13,'0')
                    #DETALLE DE LA LINEA
                    detalle = 'PA'
                    detalle += '\t' + str(rol_individual.employee_id.anterior_id).rjust(5,'0')
                    detalle += '\t' + 'USD'
                    detalle += '\t' + monto_str
                    detalle += '\t' + 'CTA'
                    detalle += '\t' + rol_individual.employee_id.bank_account_type.code
                    detalle += '\t' + rol_individual.employee_id.bank_account_id
                    detalle += '\t' + registro.payroll_id.name
                    detalle += '\t' + 'C'
                    detalle += '\t' + rol_individual.employee_id.name
                    detalle += '\t' + rol_individual.employee_id.name_related
                    detalle += '\n'
                    detalle = detalle.encode('utf-8')
                    buf_b1.write(detalle.upper())
                  if rubro.category_id.code=='NET' and rubro.total<=0:
                    #DETALLE DE LA LINEA
                    detalle = ''
                    detalle += '\t' + rol_individual.employee_id.name
                    detalle += '\t' + rol_individual.employee_id.name_related
                    detalle += '\t' + str(rubro.total)
                    detalle += '\t' + (rol_individual.employee_id.bank_id and rol_individual.employee_id.bank_id.bic or '')
                    detalle += '\t' + (rol_individual.employee_id.bank_id and rol_individual.employee_id.bank_id.name or '')
                    detalle += '\n'
                    detalle = detalle.encode('utf-8')
                    buf_b0.write(detalle.upper())
              if rol_individual.employee_id.bank_id.bic=='00002':
                for rubro in rol_individual.line_ids:
                  if rubro.category_id.code=='NET' and rubro.total>0:
                    monto=rubro.total
                    monto_str=(("%.2f"%monto).replace(".",'')).rjust(13,'0')
                    #DETALLE DE LA LINEA
                    detalle = 'PA'
                    detalle += '\t' + registro.payroll_id.name[:20]
                    detalle += '\t' + 'USD'
                    detalle += '\t' + monto_str
                    detalle += '\t' + 'CTA'
                    detalle += '\t' + rol_individual.employee_id.bank_account_type.code
                    detalle += '\t' + rol_individual.employee_id.bank_account_id
                    detalle += '\t' + registro.payroll_id.name
                    detalle += '\t' + 'C'
                    detalle += '\t' + rol_individual.employee_id.name
                    detalle += '\t' + rol_individual.employee_id.name_related
                    detalle += '\t' + '32'
                    detalle += '\n'
                    detalle = detalle.encode('utf-8')
                    buf_b2.write(detalle.upper())
                  if rubro.category_id.code=='NET' and rubro.total<=0:
                    #DETALLE DE LA LINEA
                    detalle = ''
                    detalle += '\t' + rol_individual.employee_id.name
                    detalle += '\t' + rol_individual.employee_id.name_related
                    detalle += '\t' + str(rubro.total)
                    detalle += '\t' + (rol_individual.employee_id.bank_id and rol_individual.employee_id.bank_id.bic or '')
                    detalle += '\t' + (rol_individual.employee_id.bank_id and rol_individual.employee_id.bank_id.name or '')
                    detalle += '\n'
                    detalle = detalle.encode('utf-8')
                    buf_b0.write(detalle.upper())
              if rol_individual.employee_id.bank_id.bic=='00003':
                for rubro in rol_individual.line_ids:
                  if rubro.category_id.code=='NET' and rubro.total>0:
                    monto=rubro.total
                    monto_str=(("%.2f"%monto).replace(".",'')).rjust(13,'0')
                    #DETALLE DE LA LINEA
                    detalle = 'PA'
                    detalle += '\t' + 'C'
                    detalle += '\t' + rol_individual.employee_id.name
                    detalle += '\t' + rol_individual.employee_id.name
                    detalle += '\t' + rol_individual.employee_id.name_related
                    detalle += '\t' + rol_individual.employee_id.bank_account_type.code
                    detalle += '\t' + rol_individual.employee_id.bank_account_id
                    detalle += '\t' + 'USD'
                    detalle += '\t' + monto_str
                    detalle += '\t' + '0035'
                    detalle += '\n'
                    detalle = detalle.encode('utf-8')
                    buf_b3.write(detalle.upper())
                  if rubro.category_id.code=='NET' and rubro.total<=0:
                    #DETALLE DE LA LINEA
                    detalle = ''
                    detalle += '\t' + rol_individual.employee_id.name
                    detalle += '\t' + rol_individual.employee_id.name_related
                    detalle += '\t' + str(rubro.total)
                    detalle += '\t' + (rol_individual.employee_id.bank_id and rol_individual.employee_id.bank_id.bic or '')
                    detalle += '\t' + (rol_individual.employee_id.bank_id and rol_individual.employee_id.bank_id.name or '')
                    detalle += '\n'
                    detalle = detalle.encode('utf-8')
                    buf_b0.write(detalle.upper())
              if rol_individual.employee_id.bank_id.bic not in ('00001','00002','00003'):
                for rubro in rol_individual.line_ids:
                  if rubro.category_id.code=='NET':
                    detalle = ''
                    detalle += '\t' + rol_individual.employee_id.name
                    detalle += '\t' + rol_individual.employee_id.name_related
                    detalle += '\t' + str(rubro.total)
                    detalle += '\t' + (rol_individual.employee_id.bank_id and rol_individual.employee_id.bank_id.bic or '')
                    detalle += '\t' + (rol_individual.employee_id.bank_id and rol_individual.employee_id.bank_id.name or '')
                    detalle += '\n'
                    detalle = detalle.encode('utf-8')
                    buf_b0.write(detalle.upper())
            if rol_individual.company_id.id==4 and rol_individual.employee_id.bank_id and rol_individual.employee_id.bank_account_type and rol_individual.employee_id.bank_account_id:
              if rol_individual.employee_id.bank_id.bic=='00001':
                for rubro in rol_individual.line_ids:
                  if rubro.category_id.code=='NET' and rubro.total>0:
                    monto=rubro.total
                    monto_str=(("%.2f"%monto).replace(".",'')).rjust(13,'0')
                    #DETALLE DE LA LINEA
                    detalle = 'PA'
                    detalle += '\t' + str(rol_individual.employee_id.anterior_id).rjust(5,'0')
                    detalle += '\t' + 'USD'
                    detalle += '\t' + monto_str
                    detalle += '\t' + 'CTA'
                    detalle += '\t' + rol_individual.employee_id.bank_account_type.code
                    detalle += '\t' + rol_individual.employee_id.bank_account_id
                    detalle += '\t' + registro.payroll_id.name
                    detalle += '\t' + 'C'
                    detalle += '\t' + rol_individual.employee_id.name
                    detalle += '\t' + rol_individual.employee_id.name_related
                    detalle += '\n'
                    detalle = detalle.encode('utf-8')
                    buf_c1.write(detalle.upper())
                  if rubro.category_id.code=='NET' and rubro.total<=0:
                    #DETALLE DE LA LINEA
                    detalle = ''
                    detalle += '\t' + rol_individual.employee_id.name
                    detalle += '\t' + rol_individual.employee_id.name_related
                    detalle += '\t' + str(rubro.total)
                    detalle += '\t' + (rol_individual.employee_id.bank_id and rol_individual.employee_id.bank_id.bic or '')
                    detalle += '\t' + (rol_individual.employee_id.bank_id and rol_individual.employee_id.bank_id.name or '')
                    detalle += '\n'
                    detalle = detalle.encode('utf-8')
                    buf_c0.write(detalle.upper())
              if rol_individual.employee_id.bank_id.bic=='00002':
                for rubro in rol_individual.line_ids:
                  if rubro.category_id.code=='NET' and rubro.total>0:
                    monto=rubro.total
                    monto_str=(("%.2f"%monto).replace(".",'')).rjust(13,'0')
                    #DETALLE DE LA LINEA
                    detalle = 'PA'
                    detalle += '\t' + registro.payroll_id.name[:20]
                    detalle += '\t' + 'USD'
                    detalle += '\t' + monto_str
                    detalle += '\t' + 'CTA'
                    detalle += '\t' + rol_individual.employee_id.bank_account_type.code
                    detalle += '\t' + rol_individual.employee_id.bank_account_id
                    detalle += '\t' + registro.payroll_id.name
                    detalle += '\t' + 'C'
                    detalle += '\t' + rol_individual.employee_id.name
                    detalle += '\t' + rol_individual.employee_id.name_related
                    detalle += '\t' + '32'
                    detalle += '\n'
                    detalle = detalle.encode('utf-8')
                    buf_c2.write(detalle.upper())
                  if rubro.category_id.code=='NET' and rubro.total<=0:
                    #DETALLE DE LA LINEA
                    detalle = ''
                    detalle += '\t' + rol_individual.employee_id.name
                    detalle += '\t' + rol_individual.employee_id.name_related
                    detalle += '\t' + str(rubro.total)
                    detalle += '\t' + (rol_individual.employee_id.bank_id and rol_individual.employee_id.bank_id.bic or '')
                    detalle += '\t' + (rol_individual.employee_id.bank_id and rol_individual.employee_id.bank_id.name or '')
                    detalle += '\n'
                    detalle = detalle.encode('utf-8')
                    buf_c0.write(detalle.upper())
              if rol_individual.employee_id.bank_id.bic=='00003':
                for rubro in rol_individual.line_ids:
                  if rubro.category_id.code=='NET' and rubro.total>0:
                    monto=rubro.total
                    monto_str=(("%.2f"%monto).replace(".",'')).rjust(13,'0')
                    #DETALLE DE LA LINEA
                    detalle = 'PA'
                    detalle += '\t' + 'C'
                    detalle += '\t' + rol_individual.employee_id.name
                    detalle += '\t' + rol_individual.employee_id.name
                    detalle += '\t' + rol_individual.employee_id.name_related
                    detalle += '\t' + rol_individual.employee_id.bank_account_type.code
                    detalle += '\t' + rol_individual.employee_id.bank_account_id
                    detalle += '\t' + 'USD'
                    detalle += '\t' + monto_str
                    detalle += '\t' + '0035'
                    detalle += '\n'
                    detalle = detalle.encode('utf-8')
                    buf_c3.write(detalle.upper())
                  if rubro.category_id.code=='NET' and rubro.total<=0:
                    #DETALLE DE LA LINEA
                    detalle = ''
                    detalle += '\t' + rol_individual.employee_id.name
                    detalle += '\t' + rol_individual.employee_id.name_related
                    detalle += '\t' + str(rubro.total)
                    detalle += '\t' + (rol_individual.employee_id.bank_id and rol_individual.employee_id.bank_id.bic or '')
                    detalle += '\t' + (rol_individual.employee_id.bank_id and rol_individual.employee_id.bank_id.name or '')
                    detalle += '\n'
                    detalle = detalle.encode('utf-8')
                    buf_c0.write(detalle.upper())
              if rol_individual.employee_id.bank_id.bic not in ('00001','00002','00003'):
                for rubro in rol_individual.line_ids:
                  if rubro.category_id.code=='NET':
                    detalle = ''
                    detalle += '\t' + rol_individual.employee_id.name
                    detalle += '\t' + rol_individual.employee_id.name_related
                    detalle += '\t' + str(rubro.total)
                    detalle += '\t' + (rol_individual.employee_id.bank_id and rol_individual.employee_id.bank_id.bic or '')
                    detalle += '\t' + (rol_individual.employee_id.bank_id and rol_individual.employee_id.bank_id.name or '')
                    detalle += '\n'
                    detalle = detalle.encode('utf-8')
                    buf_c0.write(detalle.upper())
          #archivos
          out_a0 = base64.encodestring(buf_a0.getvalue())
          name_a0 = "%s%s.txt" % (str(registro.payroll_id.date_end), " - ITALIMENTOS - SIN BANCO")
          self.write(cr, uid, ids, {'datas_a0': out_a0, 'datas_a0_fname': name_a0})
          buf_a0.close()

          out_b0 = base64.encodestring(buf_b0.getvalue())
          name_b0 = "%s%s.txt" % (str(registro.payroll_id.date_end), " - ITALDELI - SIN BANCO")
          self.write(cr, uid, ids, {'datas_b0': out_b0, 'datas_b0_fname': name_b0})
          buf_b0.close()
          
          out_c0 = base64.encodestring(buf_c0.getvalue())
          name_c0 = "%s%s.txt" % (str(registro.payroll_id.date_end), " - VISEMSA - SIN BANCO")
          self.write(cr, uid, ids, {'datas_c0': out_c0, 'datas_c0_fname': name_c0})
          buf_c0.close()

          out_a1 = base64.encodestring(buf_a1.getvalue())
          name_a1 = "%s%s.txt" % (str(registro.payroll_id.date_end), " - ITALIMENTOS - BANCO PICHINCHA")
          self.write(cr, uid, ids, {'datas_a1': out_a1, 'datas_a1_fname': name_a1})
          buf_a1.close()

          out_b1 = base64.encodestring(buf_b1.getvalue())
          name_b1 = "%s%s.txt" % (str(registro.payroll_id.date_end), " - ITALDELI - BANCO PICHINCHA")
          self.write(cr, uid, ids, {'datas_b1': out_b1, 'datas_b1_fname': name_b1})
          buf_b1.close()
          
          out_c1 = base64.encodestring(buf_c1.getvalue())
          name_c1 = "%s%s.txt" % (str(registro.payroll_id.date_end), " - VISEMSA - BANCO PICHINCHA")
          self.write(cr, uid, ids, {'datas_c1': out_c1, 'datas_c1_fname': name_c1})
          buf_c1.close()

          out_a2 = base64.encodestring(buf_a2.getvalue())
          name_a2 = "%s%s.txt" % (str(registro.payroll_id.date_end), " - ITALIMENTOS - BANCO INTERNACIONAL")
          self.write(cr, uid, ids, {'datas_a2': out_a2, 'datas_a2_fname': name_a2})
          buf_a2.close()

          out_b2 = base64.encodestring(buf_b2.getvalue())
          name_b2 = "%s%s.txt" % (str(registro.payroll_id.date_end), " - ITALDELI - BANCO INTERNACIONAL")
          self.write(cr, uid, ids, {'datas_b2': out_b2, 'datas_b2_fname': name_b2})
          buf_b2.close()
          
          out_c2 = base64.encodestring(buf_c2.getvalue())
          name_c2 = "%s%s.txt" % (str(registro.payroll_id.date_end), " - VISEMSA - BANCO INTERNACIONAL")
          self.write(cr, uid, ids, {'datas_c2': out_c2, 'datas_c2_fname': name_c2})
          buf_c2.close()

          out_a3 = base64.encodestring(buf_a3.getvalue())
          name_a3 = "%s%s.txt" % (str(registro.payroll_id.date_end), " - ITALIMENTOS - BANCO AUSTRO")
          self.write(cr, uid, ids, {'datas_a3': out_a3, 'datas_a3_fname': name_a3})
          buf_a3.close()

          out_b3 = base64.encodestring(buf_b3.getvalue())
          name_b3 = "%s%s.txt" % (str(registro.payroll_id.date_end), " - ITALDELI - BANCO AUSTRO")
          self.write(cr, uid, ids, {'datas_b3': out_b3, 'datas_b3_fname': name_b3})
          buf_b3.close()
          
          out_c3 = base64.encodestring(buf_c3.getvalue())
          name_c3 = "%s%s.txt" % (str(registro.payroll_id.date_end), " - VISEMSA - BANCO AUSTRO")
          self.write(cr, uid, ids, {'datas_c3': out_c3, 'datas_c3_fname': name_c3})
          buf_c3.close()

          return {
          'type': 'ir.actions.act_window',
          'name': 'Archivo Bancos',
          'view_mode': 'form',
          'view_id': False,
          'view_type': 'form',
          'res_model': 'hr.italiana.bancos',
          'res_id': registro.id,
          'nodestroy': True,
          'target': 'new',
          'context': context,
          }

hr_italiana_bancos()
