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

import time
from datetime import date
from datetime import datetime
from datetime import timedelta
from dateutil import relativedelta

from openerp import netsvc
from openerp.osv import fields, osv
from openerp import tools
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

from openerp.tools.safe_eval import safe_eval as eval
import calendar
from openerp.addons.l10n_ec_tools import easy_datetime

"""class l10n_ec_hr_payroll_configuration(osv.osv):
    _name = 'hr.payroll.configuration'
    _description = 'Configuracion de reglas para vacaciones'
    _columns = {
        'rule_biweekly': fields.many2one('hr.salary.rule', u'Regla Anticipo de quincena', required=True),
    }

l10n_ec_hr_payroll_configuration()"""

class l10n_ec_hr_salary_rule(osv.osv):
    _inherit = 'hr.salary.rule'
    _columns = {
                'living_wage': fields.boolean(u'Salario digno?', help=u'Marcar la casilla en el caso que la regla cuente como valor para el Salario Digno.'),
                'profit_type': fields.selection([('proyectar_aportable','Proyectable - Aportable'),
                                         ('proyectar_no_aportable','Proyectable - No aportable'),
                                         ('no_proyectar_aportable','No proyectable - Aportable'),
                                         ('no_proyectar_no_aportable','No proyectable - No aportable'),
                                         ('retenido','Valor retenido'),
                                         ('otros_empleadores','Otros empleadores'),
                                         ('otros_empleadores_iess','Aporte IESS otros empleadores'),
                                         ('otros_empleadores_retenido','Retenido por otros empleadores'),
                                         ('otros_valores','Otros')], u'Tipo de rentabilidad'),
                'group_debit': fields.many2one('hr.grupos_cuentas', u'Cuentas para débito'),
                'group_credit': fields.many2one('hr.grupos_cuentas', u'Cuentas para crédito'),
    }

    _order = 'sequence asc'

l10n_ec_hr_salary_rule()

class l10n_ec_hr_payslip_line(osv.osv):
    _inherit = 'hr.payslip.line'
    _columns = {
        'living_wage': fields.boolean(u'Salario digno?', help=u'Marcar la casilla en el caso que la regla cuente como valor para el Salario Digno.'),
        'profit_type': fields.selection([('proyectar_aportable','Proyectable - Aportable'),
                                         ('proyectar_no_aportable','Proyectable - No aportable'),
                                         ('no_proyectar_aportable','No proyectable - Aportable'),
                                         ('no_proyectar_no_aportable','No proyectable - No aportable'),
                                         ('retenido','Valor retenido'),
                                         ('otros_empleadores','Otros empleadores'),
                                         ('otros_empleadores_iess','Aporte IESS otros empleadores'),
                                         ('otros_empleadores_retenido','Retenido por otros empleadores'),
                                         ('otros_valores','Otros')], u'Tipo de rentabilidad'),
        'payslip_run_id': fields.related('slip_id','payslip_run_id', type='many2one', relation='hr.payslip.run', string=u'Rol general', readonly=True, store=True),
        'contract_id': fields.many2one('hr.contract', 'Contrato', required=False),
    }

    _order = 'payslip_run_id desc, slip_id asc, sequence asc'

l10n_ec_hr_payslip_line()



class l10n_ec_hr_payslip_run(osv.osv):

    _inherit = 'hr.payslip.run'

    def get_category_rules(self, cr, uid, context={}):
        obj_category = self.pool.get('hr.salary.rule.category')
        categories = obj_category.search(cr, uid, [])
        return categories

    _columns = {
#                'biweekly': fields.boolean('Anticipo Quincenal?', help='Marcar el casillero en el caso que el rol pertenezca al anticipo'),
                'payroll_type': fields.selection([('monthly', u'Mensual'),('bi-weekly', u'Quincenal'),('decimotercero', u'Décimo Tercero'),('decimocuarto', u'Décimo Cuarto'),('utilidades', u'Utilidades'),('salariodigno', u'Salario Digno')], u'Tipo de rol', required=True),
                'rule_category_ids': fields.many2many('hr.salary.rule.category','hr_paysliprun_rulecategory_rel', 'run_id', 'category_id', string=u'Categorias de entradas?', help=u'Indicar las categorias que se añadirán como entradas al rol'),
                'notes': fields.text(u'Notas'),
                'mail_result': fields.text(u'Detalle del Envio de Correos', readonly=True),
    }

    _defaults = {
                'rule_category_ids': get_category_rules,
    }

    _order = "date_end desc, name"

    def open_wizard_xls(self, cr, uid, ids, context={}):
        return {
        'type': 'ir.actions.act_window',
        'name': 'Rol general (XLS)',
        'view_mode': 'form',
        'view_id': False,
        'view_type': 'form',
        'res_model': 'hr.payroll.export',
        'nodestroy': True,
        'target': 'new',
        'context': context,
        }

    def colocar_etiquetas(self, cr, uid, ids, context={}):
        obj_payslip = self.pool.get('hr.payslip')
        obj_payslip_line = self.pool.get('hr.payslip.line')
        obj_inputs = self.pool.get('hr.payslip.input')
        for payroll in self.browse(cr, uid, ids, context=context):
            #for payslip in payroll.slip_ids:
                for payslip in payroll.slip_ids:
                    for linea in payslip.line_ids:
                        input_ids = obj_inputs.search(cr, uid, [('payslip_id','=',payslip.id),('code','=',linea.code)])
                        etiqueta = ''
                        for input_line in obj_inputs.browse(cr, uid, input_ids):
                            if len(input_ids)<=1:
                              if input_line.label:
                                etiqueta = etiqueta + " [" + str(input_line.label or '') + "]"
                            if len(input_ids)>1:
                                etiqueta = etiqueta + " [" + str(input_line.label or '') + " $" + str(input_line.amount) + "]"
                        if etiqueta:
                            etiqueta = linea.salary_rule_id.name + etiqueta
                            obj_payslip_line.write(cr, uid, linea.id, {'name': etiqueta})
        return True
    
    def enviar_emails(self, cr, uid, ids, context={}):
        resultado = ''
        obj_payslip = self.pool.get('hr.payslip')
        template_id = self.pool.get('email.template').search(cr, uid, [('name','=','Rol de Pagos de Empleado')])
        if not template_id:
            raise osv.except_osv(u'Plantilla de Correo Electrónico',  u'No existe una plantilla configurada, comuníquese con el administrador del sistema.')
        template = self.pool.get('email.template').browse(cr, uid, template_id[0])
        for this in self.browse(cr, uid, ids, context=context):
            for individual in this.slip_ids:
                #if individual.employee_id.id == 2367:
                    result = template.send_mail(individual.id, force_send=True)
                    if not result:
                        resultado += 'Error en: ' + individual.employee_id.name_complete + '\n'
        resultado += 'OK'
        return self.write(cr, uid, ids, {'mail_result': resultado})


    def close_payslip_run(self, cr, uid, ids, context={}):
        obj_payslip = self.pool.get('hr.payslip')
        obj_payslip_line = self.pool.get('hr.payslip.line')
        obj_profit = self.pool.get('hr.employee.profit')
        obj_profit_line = self.pool.get('hr.employee.profit.line')
        #contador = 0
        for payroll in self.browse(cr, uid, ids, context=context):
            for payslip in payroll.slip_ids:
                #contador +=1
                #print contador
                obj_payslip.write(cr, uid, payslip.id, {'state': 'done'}, context=context)
                for inputs in payslip.input_line_ids:
                    if inputs.io_id:
                        self.pool.get('hr.io.line').write(cr, uid, inputs.io_id.id, {'state': 'paid'}, context=context)
                """if payslip.payroll_type=='bi-weekly':
                    #self.pool.get('hr.io.line').create(cr, uid, {'state': 'send'}, context=context)
                    conf_obj = self.pool.get('hr.payroll.configuration')
                    line_obj = self.pool.get('hr.io.line')
                    line_ids = line_obj.search(cr, uid, [('biweekly_payslip_id','=',payslip.id),('state','in',['draft','send'])])
                    line_obj.write(cr, uid, line_ids,{'state':'draft'})
                    line_obj.unlink(cr, uid, line_ids, context=context)
                    conf_ids = conf_obj.search(cr, uid, [], context=context)
                    if not conf_ids:
                        raise osv.except_osv(u'Operación no permitida!', u'No existe tabla de configuración de las reglas de Quincena')
                    conf = conf_obj.browse(cr, uid, conf_ids[0], context=context)
                    total = 0
                    for linea in payslip.line_ids:
                      if linea.category_id.code in ['APT','BASIC','ING']:
                        total += linea.total
                    line_obj.create(cr, uid, {'employee_id': payslip.employee_id.id,
                                      'value': total,
                                      'rule_id': conf.rule_biweekly.id,
                                      'biweekly_payslip_id': payslip.id,
                                      'date': payslip.date_to,
                                      'biweekly': False,
                                      'state': 'send',
                                      })"""
                if payslip.payroll_type=='utilidades':
                    profit_id = obj_profit.search(cr, uid, [('employee_id','=',payslip.employee_id.id),('date_start','<=',str(payslip.date_from)),('date_stop','>=',str(payslip.date_to))], context=context)
                    if profit_id:
                        profit_id = profit_id[0]
                    else:
                        profit_id = obj_profit.create(cr, uid, {'name': str(payslip.date_to)[:4],
                                                                'employee_id': payslip.employee_id.id,
                                                                'date_start': '01/01/'+str(payslip.date_to)[:4],
                                                                'date_stop': '31/12/'+str(payslip.date_to)[:4],})
                    cr.execute("select sum(total) from hr_payslip_line where slip_id=" + str(payslip.id) + " and profit_type='no_proyectar_no_aportable'")
                    no_proyectar_no_aportable = cr.fetchone()[0] or 0.0
                    obj_profit_line.create(cr, uid, {'name':'utilidades',
                                                     'profit_id': profit_id,
                                                     'date_start': str(payslip.date_from),
                                                     'date_stop': str(payslip.date_to),
                                                     'proyectar_aportable': 0.0,
                                                     'proyectar_no_aportable': 0.0,
                                                     'no_proyectar_aportable': 0.0,
                                                     'no_proyectar_no_aportable': no_proyectar_no_aportable,
                                                     'retenido': 0.0,
                                                     'otros_empleadores': 0.0,
                                                     'otros_empleadores_iess': 0.0,
                                                     'otros_empleadores_retenido': 0.0,
                                                     'otros_valores': 0.0}, context=context)
                if payslip.payroll_type=='monthly':
                    profit_id = obj_profit.search(cr, uid, [('employee_id','=',payslip.employee_id.id),('date_start','<=',str(payslip.date_from)),('date_stop','>=',str(payslip.date_to))], context=context)
                    if profit_id:
                        profit_id = profit_id[0]
                    else:
                        profit_id = obj_profit.create(cr, uid, {'name': str(payslip.date_to)[:4],
                                                                'employee_id': payslip.employee_id.id,
                                                                'date_start': '01/01/'+str(payslip.date_to)[:4],
                                                                'date_stop': '31/12/'+str(payslip.date_to)[:4],})
                    cr.execute("select sum(total) from hr_payslip_line where slip_id=" + str(payslip.id) + " and profit_type='proyectar_aportable'")
                    proyectar_aportable = cr.fetchone()[0] or 0.0
                    cr.execute("select sum(total) from hr_payslip_line where slip_id=" + str(payslip.id) + " and profit_type='proyectar_no_aportable'")
                    proyectar_no_aportable = cr.fetchone()[0] or 0.0
                    cr.execute("select sum(total) from hr_payslip_line where slip_id=" + str(payslip.id) + " and profit_type='no_proyectar_aportable'")
                    no_proyectar_aportable = cr.fetchone()[0] or 0.0
                    cr.execute("select sum(total) from hr_payslip_line where slip_id=" + str(payslip.id) + " and profit_type='no_proyectar_no_aportable'")
                    no_proyectar_no_aportable = cr.fetchone()[0] or 0.0
                    cr.execute("select sum(total) from hr_payslip_line where slip_id=" + str(payslip.id) + " and profit_type='retenido'")
                    retenido = cr.fetchone()[0] or 0.0
                    cr.execute("select sum(total) from hr_payslip_line where slip_id=" + str(payslip.id) + " and profit_type='otros_empleadores'")
                    otros_empleadores = cr.fetchone()[0] or 0.0
                    cr.execute("select sum(total) from hr_payslip_line where slip_id=" + str(payslip.id) + " and profit_type='otros_empleadores_iess'")
                    otros_empleadores_iess = cr.fetchone()[0] or 0.0
                    cr.execute("select sum(total) from hr_payslip_line where slip_id=" + str(payslip.id) + " and profit_type='otros_empleadores_retenido'")
                    otros_empleadores_retenido = cr.fetchone()[0] or 0.0
                    cr.execute("select sum(total) from hr_payslip_line where slip_id=" + str(payslip.id) + " and profit_type='otros_valores'")
                    otros_valores = cr.fetchone()[0] or 0.0
                    cr.execute("select sum(total) from hr_payslip_line where slip_id=" + str(payslip.id) + " and code in ('IMPRENTA','IMP_RENTA')")
                    retenido = cr.fetchone()[0] or 0.0
                    if payslip.payroll_type=='monthly':
                        profit_line_id = obj_profit_line.search(cr, uid, [('profit_id','=',profit_id),('name','=','mensual'),('date_start','=',str(payslip.date_from)),('date_stop','=',str(payslip.date_to))], context=context)
                        if profit_line_id:
                            obj_profit_line.write(cr, uid, profit_line_id[0], {'proyectar_aportable': proyectar_aportable,
                                                                               'proyectar_no_aportable': proyectar_no_aportable,
                                                                               'no_proyectar_aportable': no_proyectar_aportable,
                                                                               'no_proyectar_no_aportable': no_proyectar_no_aportable,
                                                                               'retenido': retenido,
                                                                               'otros_empleadores': otros_empleadores,
                                                                               'otros_empleadores_iess': otros_empleadores_iess,
                                                                               'otros_empleadores_retenido': otros_empleadores_retenido,
                                                                               'otros_valores': otros_empleadores}, context=context)
                        else:
                            obj_profit_line.create(cr, uid, {'name':'mensual',
                                                             'profit_id': profit_id,
                                                             'date_start': str(payslip.date_from),
                                                             'date_stop': str(payslip.date_to),
                                                             'proyectar_aportable': proyectar_aportable,
                                                             'proyectar_no_aportable': proyectar_no_aportable,
                                                             'no_proyectar_aportable': no_proyectar_aportable,
                                                             'no_proyectar_no_aportable': no_proyectar_no_aportable,
                                                             'retenido': retenido,
                                                             'otros_empleadores': otros_empleadores,
                                                             'otros_empleadores_iess': otros_empleadores_iess,
                                                             'otros_empleadores_retenido': otros_empleadores_retenido,
                                                             'otros_valores': otros_empleadores}, context=context)
        #print "salio 2"
        return self.write(cr, uid, ids, {'state': 'close'}, context=context)

l10n_ec_hr_payslip_run()

class l10n_ec_hr_payslip_input(osv.osv):

    _inherit = 'hr.payslip.input'

    _columns = {
                'io_id': fields.many2one('hr.io.line',u'Ingreso/Egreso'),
                'label': fields.char(u'Etiqueta', size=50),
                'contract_id': fields.many2one('hr.contract', 'Contrato', required=False),
    }

l10n_ec_hr_payslip_input()

class l10n_ec_hr_payslip(osv.osv):

    _inherit = 'hr.payslip'

    def get_worked_day_lines(self, cr, uid, contract_ids, date_from, date_to, context=None):
        """
        @param contract_ids: list of contract id
        @return: returns a list of dict containing the input that should be applied for the given contract between date_from and date_to
        """
        def out_from_contract(contract, day):
            res = True #True indica que el día se trata de una ausencia
            if contract.date_start:
                date_start = datetime.strptime(contract.date_start, "%Y-%m-%d")
                if day >= date_start:
                    if contract.date_end:
                        date_end = datetime.strptime(contract.date_end, "%Y-%m-%d")
                        if day <= date_end:
                            res = False
                    else:
                        res = False
            return res

        def was_on_leave(employee_id, datetime_day, context=None):
            res = False
            day = datetime_day.strftime("%Y-%m-%d")
            holiday_ids = self.pool.get('hr.holidays').search(cr, uid, [('state','=','validate'),('employee_id','=',employee_id),('type','=','remove'),('date_from','<=',day),('date_to','>=',day)])
            if holiday_ids:
                #res = self.pool.get('hr.holidays').browse(cr, uid, holiday_ids, context=context)[0].holiday_status_id.name
                res = self.pool.get('hr.holidays').browse(cr, uid, holiday_ids, context=context)[0].holiday_status_id
            return res

        res = []
        for contract in self.pool.get('hr.contract').browse(cr, uid, contract_ids, context=context):
            leaves = {}
            leaves_aux = {}
            attendances = {
                 'name': 'Dias Laborados',
                 'sequence': 1,
                 'code': 'WORK100',
                 'number_of_days': 0.0,
                 'number_of_hours': 0.0,
                 'contract_id': contract.id,
            }
            day_from = datetime.strptime(date_from,"%Y-%m-%d")
            day_to = datetime.strptime(date_to,"%Y-%m-%d")
            #day_aux = datetime.strptime(date_to,"%Y-%m-%d")
            #nb_of_days = (day_to - day_from).days + 1
            bandera=False
            while bandera==False:
              nb_of_days = day_to.day
              if day_from.month==day_to.month:
                bandera=True
              else:
                ultimo_dia = calendar.monthrange(day_to.year,day_to.month)[1]
                nb_of_days = ultimo_dia
              for day in range(0, nb_of_days):
                #working_hours_on_day = self.pool.get('resource.calendar').working_hours_on_day(cr, uid, contract.working_hours, day_from + timedelta(days=day), context)
                #if working_hours_on_day:
                    #the employee had to work
                    leave_type = was_on_leave(contract.employee_id.id, day_from + timedelta(days=day), context=context)
                    leave_contract = out_from_contract(contract, day_from + timedelta(days=day))
                    #print leave_type
                    if leave_type:
                        #if he was on leave, fill the leaves dict
                        if leave_type.code in leaves:
                            leaves[leave_type.code]['number_of_days'] += 1.0
                            #leaves[leave_type]['number_of_hours'] += working_hours_on_day
                        else:
                            leaves[leave_type.code] = {
                                'name': leave_type.name,
                                'sequence': 5,
                                'code': leave_type.code,
                                'number_of_days': 1.0,
                                #'number_of_hours': working_hours_on_day,
                                'contract_id': contract.id,
                            }
                    else:
                        if leave_contract:
                            pass
                        else:
                            #add the input vals to tmp (increment if existing)
                            attendances['number_of_days'] += 1.0
                            #attendances['number_of_hours'] += working_hours_on_day
              if leaves:
                  leaves = [value for key,value in leaves.items()]
              else:
                  leaves = []
            res += [attendances] + leaves
            #print res
            aux_key = ''
            aux_value = 0
            linea_aux = False
            ultimo_dia = calendar.monthrange(day_to.year,day_to.month)[1]
            #QUITAR DOCUMENTACION PARA IGUALAR LOS DIAS A 30
            if ultimo_dia!=30 and ultimo_dia==day_to.day and ((not contract.date_end) or (contract.date_end>=date_to)) and (not datetime.strptime(contract.date_start, "%Y-%m-%d")==day_to):
                #print contract.date_end
                #print day_to
                diferencia = 30 - ultimo_dia
                bandera = False
                for linea in res:
                    if linea['code']=='WORK100' and linea['number_of_days'] >= 1:
                        linea['number_of_days'] += diferencia
                        bandera = True
                    elif linea['number_of_days'] > aux_value:
                        aux_key = linea['code']
                        aux_value = linea['number_of_days']
                if bandera==False:
                    for linea in res:
                        if linea['code']==aux_key:
                            linea['number_of_days'] += diferencia
            #print res
        return res

    def onchange_employee_id(self, cr, uid, ids, date_from, date_to, employee_id=False, contract_id=False, context=None, struct_id=False):
        empolyee_obj = self.pool.get('hr.employee')
        contract_obj = self.pool.get('hr.contract')
        worked_days_obj = self.pool.get('hr.payslip.worked_days')
        input_obj = self.pool.get('hr.payslip.input')

        if context is None:
            context = {}
        #delete old worked days lines
        old_worked_days_ids = ids and worked_days_obj.search(cr, uid, [('payslip_id', '=', ids[0])], context=context) or False
        if old_worked_days_ids:
            worked_days_obj.unlink(cr, uid, old_worked_days_ids, context=context)

        #delete old input lines
        old_input_ids = ids and input_obj.search(cr, uid, [('payslip_id', '=', ids[0])], context=context) or False
        if old_input_ids:
            input_obj.unlink(cr, uid, old_input_ids, context=context)


        #defaults
        res = {'value':{
                      'line_ids':[],
                      'input_line_ids': [],
                      'worked_days_line_ids': [],
                      #'details_by_salary_head':[], TODO put me back
                      'name':'',
                      'contract_id': False,
                      'struct_id': False,
                      }
            }
        if (not employee_id) or (not date_from) or (not date_to):
            return res
        ttyme = datetime.fromtimestamp(time.mktime(time.strptime(date_from, "%Y-%m-%d")))
        employee_id = empolyee_obj.browse(cr, uid, employee_id, context=context)
        res['value'].update({
                    'name': _('Salary Slip of %s for %s') % (employee_id.name, tools.ustr(ttyme.strftime('%B-%Y'))),
                    'company_id': employee_id.company_id.id
        })

        if not context.get('contract', False):
            #fill with the first contract of the employee
            contract_ids = self.get_contract(cr, uid, employee_id, date_from, date_to, context=context)
        else:
            if contract_id:
                #set the list of contract for which the input have to be filled
                contract_ids = [contract_id]
            else:
                #if we don't give the contract, then the input to fill should be for all current contracts of the employee
                contract_ids = self.get_contract(cr, uid, employee_id, date_from, date_to, context=context)

        if not contract_ids:
            res['value'].update({'struct_id': struct_id and struct_id or False,})
            contract_ids = []
            if employee_id.contract_id:
                contract_ids = employee_id.contract_id.id
                res['value'].update({'contract_id': employee_id.contract_id.id, 'company_id': employee_id.contract_id.company_id and employee_id.contract_id.company_id.id or False})
                input_line_ids = self.get_inputs(cr, uid, contract_ids, date_from, date_to, context=context)
            else:
                res['value'].update({'company_id':employee_id.company_id and employee_id.company_id.id or False})
                input_line_ids = self.get_inputs(cr, uid, [], date_from, date_to, context=context, employee_id=employee_id.id)
            res['value'].update({'input_line_ids':input_line_ids })
            return res
        contract_record = contract_obj.browse(cr, uid, contract_ids[0], context=context)
        res['value'].update({
                    'contract_id': contract_record and contract_record.id or False,
                    'company_id': contract_record.company_id.id or False
        })
        struct_record = contract_record and contract_record.struct_id or False
        if not struct_record:
            return res
        res['value'].update({
                    'struct_id': struct_record.id,
        })
        #computation of the salary input
        worked_days_line_ids = self.get_worked_day_lines(cr, uid, contract_ids, date_from, date_to, context=context)
        input_line_ids = self.get_inputs(cr, uid, contract_ids, date_from, date_to, context=context)
        res['value'].update({
                    'worked_days_line_ids': worked_days_line_ids,
                    'input_line_ids': input_line_ids,
        })
        return res

    def get_inputs(self, cr, uid, contract_ids, date_from, date_to, context=None, employee_id=False):
        res = []
        contract_obj = self.pool.get('hr.contract')
        employee_obj = self.pool.get('hr.employee')
        rule_obj = self.pool.get('hr.salary.rule')

        structure_ids = contract_obj.get_all_structures(cr, uid, contract_ids, context=context)
        rule_ids = self.pool.get('hr.payroll.structure').get_all_rules(cr, uid, structure_ids, context=context)
        sorted_rule_ids = [id for id, sequence in sorted(rule_ids, key=lambda x:x[1])]

        for contract in contract_obj.browse(cr, uid, contract_ids, context=context):
            for rule in rule_obj.browse(cr, uid, sorted_rule_ids, context=context):
                if rule.input_ids:
                    for input in rule.input_ids:
                        inputs = {
                             'name': input.name,
                             'code': input.code,
                             'contract_id': contract.id,
                        }
                        res += [inputs]
        #ADD INPUTS HEREEEEEE
        #import pdb
        #pdb.set_trace()
        if context.has_key('rule_category_ids'):
            io_line_obj = self.pool.get('hr.io.line')
            #for payslip in self.browse(cr, uid, ids):
            for contract in contract_obj.browse(cr, uid, contract_ids, context=context):
                io_ids = []
                io_ids = io_line_obj.search(cr, uid, [('employee_id', '=', contract.employee_id.id),
                                                      ('date', '>=', date_from),
                                                      ('date', '<=', date_to),
                                                      ('state', '=', 'send')])
                if context.has_key('payroll_type'):
                    if context['payroll_type']=='bi-weekly':
                        io_ids = io_line_obj.search(cr, uid, [('employee_id', '=', contract.employee_id.id),
                                                      ('date', '>=', date_from),
                                                      ('date', '<=', date_to),
                                                      ('biweekly', '=', True),
                                                      ('state', '=', 'send')])
                for io in io_line_obj.browse(cr, uid, io_ids, context=context):
                    if io.rule_id.category_id.id in context['rule_category_ids']:
                        inputs = {
                                  'name': io.rule_id.name,
                                  'code': io.rule_id.code,
                                  'label': io.label,
                                  'contract_id': contract.id,
                                  'io_id': io.id,
                                  'amount': io.value,
                                  }
                        res += [inputs]
            if employee_id:
                io_ids = []
                io_ids = io_line_obj.search(cr, uid, [('employee_id', '=', employee_id),
                                                      ('date', '>=', date_from),
                                                      ('date', '<=', date_to),
                                                      ('state', '=', 'send')])
                for io in io_line_obj.browse(cr, uid, io_ids, context=context):
                    if io.rule_id.category_id.id in context['rule_category_ids']:
                        inputs = {
                                  'name': io.rule_id.name,
                                  'code': io.rule_id.code,
                                  'label': io.label,
                                  #'contract_id': contract.id,
                                  'io_id': io.id,
                                  'amount': io.value,
                                  }
                        res += [inputs]
        return res

    def compute_sheet(self, cr, uid, ids, context=None):
        slip_line_pool = self.pool.get('hr.payslip.line')
        sequence_obj = self.pool.get('ir.sequence')
        for payslip in self.browse(cr, uid, ids, context=context):
            number = payslip.number or sequence_obj.get(cr, uid, 'salary.slip')
            #delete old payslip lines
            old_slipline_ids = slip_line_pool.search(cr, uid, [('slip_id', '=', payslip.id)], context=context)
#            old_slipline_ids
            if old_slipline_ids:
                slip_line_pool.unlink(cr, uid, old_slipline_ids, context=context)
            if payslip.contract_id:
                #set the list of contract for which the rules have to be applied
                contract_ids = [payslip.contract_id.id]
            else:
                #if we don't give the contract, then the rules to apply should be for all current contracts of the employee
                contract_ids = self.get_contract(cr, uid, payslip.employee_id, payslip.date_from, payslip.date_to, context=context)
            lines = [(0,0,line) for line in self.pool.get('hr.payslip').get_payslip_lines(cr, uid, contract_ids, payslip.id, context=context, employee_id=payslip.employee_id.id)]
            self.write(cr, uid, [payslip.id], {'line_ids': lines, 'number': number,}, context=context)
        return True

    def get_payslip_lines(self, cr, uid, contract_ids, payslip_id, context, employee_id=False):
        def _sum_salary_rule_category(localdict, category, amount):
            if category.parent_id:
                localdict = _sum_salary_rule_category(localdict, category.parent_id, amount)
            localdict['categories'].dict[category.code] = category.code in localdict['categories'].dict and localdict['categories'].dict[category.code] + amount or amount
            return localdict

        class BrowsableObject(object):
            def __init__(self, pool, cr, uid, employee_id, dict):
                self.pool = pool
                self.cr = cr
                self.uid = uid
                self.employee_id = employee_id
                self.dict = dict

            def __getattr__(self, attr):
                return attr in self.dict and self.dict.__getitem__(attr) or 0.0

        class InputLine(BrowsableObject):
            """a class that will be used into the python code, mainly for usability purposes"""
            def sum(self, code, from_date, to_date=None):
                if to_date is None:
                    to_date = datetime.now().strftime('%Y-%m-%d')
                result = 0.0
                self.cr.execute("SELECT sum(amount) as sum\
                            FROM hr_payslip as hp, hr_payslip_input as pi \
                            WHERE hp.employee_id = %s AND hp.state = 'done' \
                            AND hp.date_from >= %s AND hp.date_to <= %s AND hp.id = pi.payslip_id AND pi.code = %s",
                           (self.employee_id, from_date, to_date, code))
                res = self.cr.fetchone()[0]
                return res or 0.0

        class WorkedDays(BrowsableObject):
            """a class that will be used into the python code, mainly for usability purposes"""
            def _sum(self, code, from_date, to_date=None, company_id=None):
                if to_date is None:
                    to_date = datetime.now().strftime('%Y-%m-%d')
                result = 0.0
                if company_id is None:
                    self.cr.execute("SELECT sum(number_of_days) as number_of_days, sum(number_of_hours) as number_of_hours\
                            FROM hr_payslip as hp, hr_payslip_worked_days as pi \
                            WHERE hp.employee_id = %s AND hp.state = 'done' AND hp.payroll_type = 'monthly' \
                            AND hp.date_from >= %s AND hp.date_to <= %s AND hp.id = pi.payslip_id AND pi.code = %s",
                           (self.employee_id, from_date, to_date, code))
                else:
                    self.cr.execute("SELECT sum(number_of_days) as number_of_days, sum(number_of_hours) as number_of_hours\
                            FROM hr_payslip as hp, hr_payslip_worked_days as pi \
                            WHERE hp.employee_id = %s AND hp.state = 'done' AND hp.payroll_type = 'monthly' \
                            AND hp.date_from >= %s AND hp.date_to <= %s AND hp.id = pi.payslip_id AND pi.code = %s AND hp.company_id = %s",
                           (self.employee_id, from_date, to_date, code, company_id))
                return self.cr.fetchone()

            def sum(self, code, from_date, to_date=None, company_id=None):
                res = self._sum(code, from_date, to_date, company_id)
                return res and res[0] or 0.0

            def sum_hours(self, code, from_date, to_date=None):
                res = self._sum(code, from_date, to_date)
                return res and res[1] or 0.0

        class Payslips(BrowsableObject):
            """a class that will be used into the python code, mainly for usability purposes"""

            def sum(self, code, from_date, to_date=None, contract_id=None, living_wage=None):
                if to_date is None:
                    to_date = datetime.now().strftime('%Y-%m-%d')
                if living_wage is None:
                    if contract_id is None:
                        self.cr.execute("SELECT sum(case when hp.credit_note = False then (pl.total) else (-pl.total) end)\
                                FROM hr_payslip as hp, hr_payslip_line as pl \
                                WHERE hp.employee_id = %s AND hp.state = 'done' \
                                AND hp.date_from >= %s AND hp.date_to <= %s AND hp.id = pl.slip_id AND pl.code = %s",
                                (self.employee_id, from_date, to_date, code))
                    else:
                        self.cr.execute("SELECT sum(case when hp.credit_note = False then (pl.total) else (-pl.total) end)\
                                FROM hr_payslip as hp, hr_payslip_line as pl \
                                WHERE hp.employee_id = %s AND hp.state = 'done' \
                                AND hp.date_from >= %s AND hp.date_to <= %s AND hp.id = pl.slip_id AND pl.code = %s AND hp.contract_id = %s",
                                (self.employee_id, from_date, to_date, code, contract_id))
                else:
                    #tomamos el contrato como compañia
                    if contract_id is None:
                        self.cr.execute("SELECT sum(case when hp.credit_note = False then (pl.total) else (-pl.total) end)\
                                FROM hr_payslip as hp, hr_payslip_line as pl \
                                WHERE hp.employee_id = %s AND hp.state = 'done' \
                                AND hp.date_from >= %s AND hp.date_to <= %s AND hp.id = pl.slip_id AND pl.living_wage = %s",
                                (self.employee_id, from_date, to_date, True))
                    else:
                        self.cr.execute("SELECT sum(case when hp.credit_note = False then (pl.total) else (-pl.total) end)\
                                FROM hr_payslip as hp, hr_payslip_line as pl \
                                WHERE hp.employee_id = %s AND hp.state = 'done' \
                                AND hp.date_from >= %s AND hp.date_to <= %s AND hp.id = pl.slip_id AND pl.living_wage = %s AND hp.company_id = %s",
                                (self.employee_id, from_date, to_date, True, contract_id))
                res = self.cr.fetchone()
                return res and res[0] or 0.0

        class ec_sri(BrowsableObject):
            def tabla_base(self, fecha):
                obj_tabla = self.pool.get('hr.sri.taxable')
                tabla_ids = obj_tabla.search(self.cr, self.uid, [('date_start','<=',fecha),('date_stop','>=',fecha)])
                if tabla_ids:
                    tabla = obj_tabla.browse(self.cr, self.uid, tabla_ids[0])
                    return tabla
                return False
            
        class ec_utilidades(BrowsableObject):
            def total_dias(self, code, from_date, to_date, company_id):
                if to_date is None:
                    to_date = datetime.now().strftime('%Y-%m-%d')
                self.cr.execute("SELECT sum(d.number_of_days) FROM hr_payslip p \
                INNER JOIN hr_payslip_worked_days d ON d.payslip_id=p.id \
                WHERE p.payroll_type='monthly' \
                AND p.employee_id not in (2909,2228) \
                AND d.code in %s \
                AND p.company_id = %s \
                AND p.date_from >= %s \
                AND p.date_to <= %s ",
                                (code, company_id, from_date, to_date))
                res = self.cr.fetchone()
                return res and res[0] or 0.0
            def total_entrada(self, employee_id, from_date, to_date, code):
                if to_date is None:
                    to_date = datetime.now().strftime('%Y-%m-%d')
                self.cr.execute("SELECT sum(io.value) FROM hr_io_line io \
                INNER JOIN hr_salary_rule r on r.id=io.rule_id \
                WHERE io.state='send' \
                AND io.employee_id=%s \
                AND io.date >= %s \
                AND io.date <= %s \
                AND r.code = %s ",
                                (employee_id, from_date, to_date, code))
                res = self.cr.fetchone()
                return res and res[0] or 0.0
            def total_cargas(self, from_date, to_date, company_id, max_birthday):
                if to_date is None:
                    to_date = datetime.now().strftime('%Y-%m-%d')
                self.cr.execute("select count(distinct(f.id)) from hr_payslip p \
                INNER JOIN hr_employee_family f ON f.employee_id=p.employee_id \
                WHERE p.payroll_type='monthly' \
                AND f.employee_id not in (2909,2228) \
                AND (f.birthday >= %s OR f.relationship_id in (10,13)) \
                AND p.company_id = %s \
                AND p.date_from >= %s \
                AND p.date_to <= %s ",
                                (max_birthday, company_id, from_date, to_date))
                res = self.cr.fetchone()
                return res and res[0] or 0.0
            def cargas_complementarios(self, company_id, max_birthday):
                self.cr.execute("select count(f.id) from hr_employee e \
                INNER JOIN resource_resource r ON r.id=e.resource_id \
                INNER JOIN hr_employee_family f ON f.employee_id=e.id \
                WHERE r.company_id = %s \
                AND (f.birthday >= %s OR f.relationship_id in (10,13)) \
                AND r.active= %s \
                and e.servicios_complementarios = %s ",(company_id,max_birthday, True,True))
                res = self.cr.fetchone()
                return res and res[0] or 0.0

        class ec_contract(BrowsableObject):
            def search(self, parameters):
                return self.pool.get("hr.contract").search(self.cr, self.uid, parameters)
            def browse(self, ids):
                return self.pool.get("hr.contract").browse(self.cr, self.uid, ids)

        class ec_employee(BrowsableObject):
            def search(self, parameters):
                return self.pool.get("hr.employee").search(self.cr, self.uid, parameters)
            def browse(self, ids):
                return self.pool.get("hr.employee").browse(self.cr, self.uid, ids)

        #we keep a dict with the result because a value can be overwritten by another rule with the same code
        result_dict = {}
        rules = {}
        categories_dict = {}
        blacklist = []
        payslip_obj = self.pool.get('hr.payslip')
        inputs_obj = self.pool.get('hr.payslip.worked_days')
        obj_rule = self.pool.get('hr.salary.rule')
        payslip = payslip_obj.browse(cr, uid, payslip_id, context=context)
        worked_days = {}
        for worked_days_line in payslip.worked_days_line_ids:
            worked_days[worked_days_line.code] = worked_days_line
        inputs = {}
        for input_line in payslip.input_line_ids:
            if inputs.has_key(input_line.code):
                inputs[input_line.code].amount +=  input_line.amount
            else:
                inputs[input_line.code] = input_line

        categories_obj = BrowsableObject(self.pool, cr, uid, payslip.employee_id.id, categories_dict)
        input_obj = InputLine(self.pool, cr, uid, payslip.employee_id.id, inputs)
        worked_days_obj = WorkedDays(self.pool, cr, uid, payslip.employee_id.id, worked_days)
        payslip_obj = Payslips(self.pool, cr, uid, payslip.employee_id.id, payslip)
        rules_obj = BrowsableObject(self.pool, cr, uid, payslip.employee_id.id, rules)

        ec_sri_obj = ec_sri(self.pool, cr, uid, payslip.employee_id.id, {})
        ec_contract_obj = ec_contract(self.pool, cr, uid, payslip.employee_id.id, {})
        ec_employee_obj = ec_employee(self.pool, cr, uid, payslip.employee_id.id, {})
        ec_utilidades_obj = ec_utilidades(self.pool, cr, uid, payslip.employee_id.id, {})

        baselocaldict = {'categories': categories_obj, 'rules': rules_obj, 'payslip': payslip_obj, 'worked_days': worked_days_obj, 'inputs': input_obj, 'easy_datetime': easy_datetime, 'ec_sri': ec_sri_obj, 'ec_contract': ec_contract_obj, 'ec_employee': ec_employee_obj, 'ec_utilidades': ec_utilidades_obj}

        #Here we get salary structure
        structure_ids = []
        if context.has_key('different_structure'):
            #get the id of the structure in the wizard
            if context['different_structure']!=False:
                structure_ids = [context['different_structure'][0]]
                structure_ids = list(set(self.pool.get('hr.payroll.structure')._get_parent_structure(cr, uid, structure_ids, context=context)))
            else:
                structure_ids = self.pool.get('hr.contract').get_all_structures(cr, uid, contract_ids, context=context)
        else:
            #get the ids of the structures on the contracts and their parent id as well
            structure_ids = self.pool.get('hr.contract').get_all_structures(cr, uid, contract_ids, context=context)

        #get the rules of the structure and thier children
        rule_ids = self.pool.get('hr.payroll.structure').get_all_rules(cr, uid, structure_ids, context=context)
        #run the rules by sequence
        sorted_rule_ids = [id for id, sequence in sorted(rule_ids, key=lambda x:x[1])]

        #import pdb
        #pdb.set_trace()
        for contract in self.pool.get('hr.contract').browse(cr, uid, contract_ids, context=context):
            #if context.has_key('payroll_type'):
            #    if context['payroll_type']=='bi-weekly':
            #        if contract.date_end:
            #          #if contract.date_end<=self.pool.get('hr.payslip.run').browse(cr, uid, payslip_id, context=context).date_end:
            #            continue
            employee = contract.employee_id
            localdict = dict(baselocaldict, employee=employee, contract=contract, living_wage=0.0)
            for rule in obj_rule.browse(cr, uid, sorted_rule_ids, context=context):
                key = rule.code + '-' + str(contract.id)
                localdict['result'] = None
                localdict['result_qty'] = 1.0
                localdict['result_rate'] = 100
                #check if the rule can be applied
                if obj_rule.satisfy_condition(cr, uid, rule.id, localdict, context=context) and rule.id not in blacklist:
                    #compute the amount of the rule
                    amount, qty, rate = obj_rule.compute_rule(cr, uid, rule.id, localdict, context=context)
                    #check if there is already a rule computed with that code
                    previous_amount = rule.code in localdict and localdict[rule.code] or 0.0
                    #set/overwrite the amount computed for this rule in the localdict
                    tot_rule = amount * qty * rate / 100.0
                    localdict[rule.code] = tot_rule
                    rules[rule.code] = rule
                    #add living_wage value to localdict
                    if rule.living_wage:
                        localdict['living_wage'] += amount
                    #sum the amount for its salary category
                    localdict = _sum_salary_rule_category(localdict, rule.category_id, tot_rule - previous_amount)
                    #create/overwrite the rule in the temporary results
                    #import pdb
                    #pdb.set_trace()
                    result_dict[key] = {
                        'salary_rule_id': rule.id,
                        'contract_id': contract.id,
                        'name': rule.name,
                        'code': rule.code,
                        'category_id': rule.category_id.id,
                        'sequence': rule.sequence,
                        'appears_on_payslip': rule.appears_on_payslip,
                        'condition_select': rule.condition_select,
                        'condition_python': rule.condition_python,
                        'condition_range': rule.condition_range,
                        'condition_range_min': rule.condition_range_min,
                        'condition_range_max': rule.condition_range_max,
                        'amount_select': rule.amount_select,
                        'amount_fix': rule.amount_fix,
                        'amount_python_compute': rule.amount_python_compute,
                        'amount_percentage': rule.amount_percentage,
                        'amount_percentage_base': rule.amount_percentage_base,
                        'register_id': rule.register_id.id,
                        'amount': amount,
                        'employee_id': contract.employee_id.id,
                        'quantity': qty,
                        'rate': rate,
                        'living_wage': rule.living_wage,
                        'profit_type': rule.profit_type,
                    }
                else:
                    #blacklist this rule and its children
                    blacklist += [id for id, seq in self.pool.get('hr.salary.rule')._recursive_search_of_rules(cr, uid, [rule], context=context)]
        if employee_id and not contract_ids:
            #if context.has_key('payroll_type'):
            #    if context['payroll_type']=='bi-weekly':
            #        if contract.date_end:
            #          #if contract.date_end<=self.pool.get('hr.payslip.run').browse(cr, uid, payslip_id, context=context).date_end:
            #            continue
            employee = self.pool.get('hr.employee').browse(cr, uid, employee_id)
            localdict = dict(baselocaldict, employee=employee, contract=False, living_wage=0.0)
            for rule in obj_rule.browse(cr, uid, sorted_rule_ids, context=context):
                key = rule.code + '-' + str('')
                localdict['result'] = None
                localdict['result_qty'] = 1.0
                localdict['result_rate'] = 100
                #check if the rule can be applied
                if obj_rule.satisfy_condition(cr, uid, rule.id, localdict, context=context) and rule.id not in blacklist:
                    #compute the amount of the rule
                    amount, qty, rate = obj_rule.compute_rule(cr, uid, rule.id, localdict, context=context)
                    #check if there is already a rule computed with that code
                    previous_amount = rule.code in localdict and localdict[rule.code] or 0.0
                    #set/overwrite the amount computed for this rule in the localdict
                    tot_rule = amount * qty * rate / 100.0
                    localdict[rule.code] = tot_rule
                    rules[rule.code] = rule
                    #add living_wage value to localdict
                    if rule.living_wage:
                        localdict['living_wage'] += amount
                    #sum the amount for its salary category
                    localdict = _sum_salary_rule_category(localdict, rule.category_id, tot_rule - previous_amount)
                    #create/overwrite the rule in the temporary results
                    #import pdb
                    #pdb.set_trace()
                    result_dict[key] = {
                        'salary_rule_id': rule.id,
                        'contract_id': False,
                        'name': rule.name,
                        'code': rule.code,
                        'category_id': rule.category_id.id,
                        'sequence': rule.sequence,
                        'appears_on_payslip': rule.appears_on_payslip,
                        'condition_select': rule.condition_select,
                        'condition_python': rule.condition_python,
                        'condition_range': rule.condition_range,
                        'condition_range_min': rule.condition_range_min,
                        'condition_range_max': rule.condition_range_max,
                        'amount_select': rule.amount_select,
                        'amount_fix': rule.amount_fix,
                        'amount_python_compute': rule.amount_python_compute,
                        'amount_percentage': rule.amount_percentage,
                        'amount_percentage_base': rule.amount_percentage_base,
                        'register_id': rule.register_id.id,
                        'amount': amount,
                        'employee_id': employee.id,
                        'quantity': qty,
                        'rate': rate,
                        'living_wage': rule.living_wage,
                        'profit_type': rule.profit_type,
                    }
                else:
                    #blacklist this rule and its children
                    blacklist += [id for id, seq in self.pool.get('hr.salary.rule')._recursive_search_of_rules(cr, uid, [rule], context=context)]
        result = [value for code, value in result_dict.items()]
        return result

    def _compute_values(self, cr, uid, ids, fields, args, context):
        res = {}
        for obj in self.browse(cr, uid, ids, context):
            res[obj.id] = {
                           'total': 0.0,
                          }
            for line in obj.line_ids:
                if line.category_id.code == 'NET':
                    res[obj.id]['total'] = line.total
        return res

    def _get_payslip_lines(self, cr, uid, ids, context):
        res = {}
        for obj in self.pool.get('hr.payslip.line').browse(cr, uid, ids, context):
            if obj.code=='NET':
                res[obj.slip_id.id] = True
        return res.keys()

    STORE_VAR = {'hr.payslip.line': (_get_payslip_lines, ['total'], 10),}

    _columns = {
#       'biweekly': fields.boolean('Anticipo Quincenal?', help='Marcar el casillero en el caso que el rol pertenezca al anticipo'),
        'payroll_type': fields.selection([('monthly', u'Mensual'),('bi-weekly', u'Quincenal'),('decimotercero', u'Décimo Tercero'),('decimocuarto', u'Décimo Cuarto'),('utilidades', u'Utilidades'),('salariodigno', u'Salario Digno')], u'Tipo de rol', required=True, readonly=True),
        'payslip_run_id': fields.many2one('hr.payslip.run', u'Payslip Batches', readonly=True, states={'draft': [('readonly', False)]}, ondelete='cascade'),
        'job_id': fields.related('contract_id','job_id', type='many2one', relation='hr.job', string=u'Puesto de Trabajo', readonly=True, store=True),
        'department_id': fields.related('contract_id','department_id', type='many2one', relation='hr.department', string=u'Departamento', readonly=True, store=True),
        'total': fields.function(_compute_values, method=True, string=u'Total', readonly=True, store=False, multi='payslip'),
        'employee_category_id': fields.many2one('hr.employee.category', u'Categoría de empleado', readonly=True),
        'city_id': fields.related('contract_id','city_id',type='many2one',relation='res.country.state.city', string=u'Ciudad', store=True),
        #'company_id': fields.related('contract_id','company_id',type='many2one',relation='res.company', string=u'Empresa', store=True),
       }

    _order = "date_to desc, payslip_run_id desc, number asc"

l10n_ec_hr_payslip()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
