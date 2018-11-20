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

from openerp.osv import osv, fields

from openerp.addons.l10n_ec_tools import easy_datetime
from datetime import date, datetime, timedelta
from time import strftime
import openerp.addons.decimal_precision as dp


class hr_liquidation_rule(osv.osv):
    _inherit = 'hr.salary.rule'
    _name = 'hr.liquidation.rule'
    
    _columns = {
                'name':fields.char('Nombre', size=256, required=True, readonly=False),
                'code':fields.char('Código', size=64, required=True, help="El código de las reglas puede usarse como referencia en el computo de otras reglas. Por esta razón se distingue de mayusculas y minusculas"),
                'category_id':fields.many2one('hr.salary.rule.category', 'Categoria', required=True),
                'sequence': fields.integer('Secuencia', required=True, help='Usado para ordenar la secuencia de calculo', select=True),
                'active':fields.boolean('Activo'),
                'appears_on_payslip': fields.boolean('Aparece en Liquidación?', help="Usado para mostrar la regla en la liquidación"),
                'quantity': fields.char('Cantidad', size=256, help="Es usado para el computo de porcentaje o monto fijo."),
                'condition_select': fields.selection([('none', 'Siempre verdadero'),('range', 'Rango'), ('python', 'Expresión Python')], "Condición basada en", required=True),
                'condition_range':fields.char('Rango basado en',size=1024, readonly=False, help='This will be used to compute the % fields values; in general it is on basic, but you can also use categories code fields in lowercase as a variable names (hra, ma, lta, etc.) and the variable basic.'),
                'condition_python':fields.text('Condición Python', required=True, readonly=False, help='Aplica la regla de calculo si esta condición es verdadera. Puede especificar la condición como basic > 1000.'),
                'condition_range_min': fields.float('Rango Minimo', required=False, help="El monto minimo, aplicado para esta regla."),
                'condition_range_max': fields.float('Rango Maximo', required=False, help="El monto maximo, aplicado para esta regla."),
                'amount_select':fields.selection([
                                                  ('percentage','Porcentaje (%)'),
                                                  ('fix','Monto Fijo'),
                                                  ('code','Código Python'),
                                                  ],'Tipo de Monto', select=True, required=True, help="El metodo de computo para el valor de la regla."),
                'amount_fix': fields.float('Monto Fijo', digits_compute=dp.get_precision('Payroll'),),
                'amount_percentage': fields.float('Porcentaje (%)', digits_compute=dp.get_precision('Payroll Rate'), help='Por ejemplo, ingresar 50.0  para aplicar el 50%'),
                'amount_python_compute':fields.text('Código Python'),
                'amount_percentage_base':fields.char('Porcentaje basado en',size=1024, required=False, readonly=False, help='El resultado es afectado por una variable'),
                'note':fields.text('Descripción'),
                }
    
hr_liquidation_rule()

class hr_liquidation_structure(osv.osv):
    """
    Liquidation structure used to defined
    - Basic
    - Allowances
    - Deductions
    """

    _name = 'hr.liquidation.structure'
    _description = 'Estructura de liquidación'
    _columns = {
        'name':fields.char('Nombre', size=256, required=True),
        'active': fields.boolean('Activo', help="Activarlo si este tipo de liquidación se encuentra activa."),
        #'code':fields.char('Reference', size=64, required=True),
        #'company_id':fields.many2one('res.company', 'Company', required=True),
        'note': fields.text('Descripción'),
        'parent_id':fields.many2one('hr.payroll.structure', 'Padre'),
        'children_ids':fields.one2many('hr.payroll.structure', 'parent_id', 'Hijas'),
        'rule_ids':fields.many2many('hr.liquidation.rule', 'hr_structure_liquidation_rule_rel', 'struct_id', 'rule_id', 'Reglas'),
    }
    
    _defaults = {
                 'active':True
                 }
    
    def get_all_rules(self, cr, uid, structure_ids, context=None):
        """
        @param structure_ids: list of structure
        @return: returns a list of tuple (id, sequence) of rules that are maybe to apply
        """
        all_rules = []
        for struct in self.browse(cr, uid, structure_ids, context=context):
            all_rules += self.pool.get('hr.liquidation.rule')._recursive_search_of_rules(cr, uid, struct.rule_ids, context=context)
        return all_rules

hr_liquidation_structure()

class hr_liquidation_input(osv.osv):
    '''
    Liquidation Input
    '''

    _name = 'hr.liquidation.input'
    _description = 'Entradas de liquidación'
    _columns = {
        'name': fields.char('Descripción', size=256, required=True),
        'payslip_id': fields.many2one('hr.liquidation.compute', 'Liquidación', required=True, ondelete='cascade', select=True),
        'sequence': fields.integer('Secuencia', required=True, select=True),
        'code': fields.char('Código', size=52, required=True),
        'amount': fields.float('Monto'),
    }
    _order = 'payslip_id, sequence'
    _defaults = {
        'sequence': 10,
        'amount': 0.0,
    }

hr_liquidation_input()

class one2many_mod2(fields.one2many):

    def get(self, cr, obj, ids, name, user=None, offset=0, context=None, values=None):
        if context is None:
            context = {}
        if not values:
            values = {}
        res = {}
        for id in ids:
            res[id] = []
        ids2 = obj.pool[self._obj].search(cr, user, [(self._fields_id,'in',ids), ('appears_on_payslip', '=', True)], limit=self._limit)
        for r in obj.pool[self._obj].read(cr, user, ids2, [self._fields_id], context=context, load='_classic_write'):
            key = r[self._fields_id]
            if isinstance(key, tuple):
                # Read return a tuple in the case where the field is a many2one
                # but we want to get the id of this field.
                key = key[0]

            res[key].append( r['id'] )
        return res

class hr_liquidation_compute(osv.osv):
    _name = "hr.liquidation.compute"
    
    _columns = {
                #'name': fields.char('Código', size=20, required=True),
                'description': fields.text('Descripción', size=100),
                'date': fields.date('Fecha de Salida', required=True),
                'contract_id': fields.many2one('hr.contract','Contrato de empleado', required=True),
                'employee_id' :  fields.related('contract_id','employee_id', type='many2one', relation='hr.employee', string=u'Empleado', readonly=True, store=True),
                'structure_id': fields.many2one('hr.liquidation.structure','Motivo de Salida', required=True),
                'state': fields.selection([('draft','Borrador'),
                                           ('done','Aprobado'),
                                           ('cancel','Terminado')],'Estado'),
                'line_ids': one2many_mod2('hr.liquidation.line', 'liquidation_id', 'Lineas de Liquidación', readonly=True),
                
                #'worked_days_line_ids': fields.one2many('hr.payslip.worked_days', 'payslip_id', 'Payslip Worked Days', required=False, readonly=True, states={'draft': [('readonly', False)]}),
                'input_line_ids': fields.one2many('hr.liquidation.input', 'payslip_id', 'Entradas de Liquidación', required=False),
                'mujer_embarazada': fields.boolean('Es mujer embarazada?', help='Active el casillero si se trata de una mujer embarazada'),
                'jefe_sindical': fields.boolean('Es jefe sindical?', help='Active el casillero si se trata de un jefe sindical'),
                'empleador_iess': fields.boolean('Empleador asume IESS?', help='Active el casillero si el empleador asume el valor a pagar al IESS'),
                }
    
    _defaults = {
                 'state': 'draft'
                 }
    
    _order = 'date, employee_id'
    
    def calcular_liquidacion(self, cr, uid, ids, context=None):
        slip_line_pool = self.pool.get('hr.liquidation.line')
        #sequence_obj = self.pool.get('ir.sequence')
        for liquidacion in self.browse(cr, uid, ids, context=context):
            #number = payslip.number or sequence_obj.get(cr, uid, 'salary.slip')
            #delete old payslip lines
            old_slipline_ids = slip_line_pool.search(cr, uid, [('liquidation_id', '=', liquidacion.id)], context=context)
#            old_slipline_ids
            if old_slipline_ids:
                slip_line_pool.unlink(cr, uid, old_slipline_ids, context=context)
            contract_ids = [liquidacion.contract_id.id]
            # continuar de aqui en adelante
            lines = [(0,0,line) for line in self.pool.get('hr.liquidation.compute').get_payslip_lines(cr, uid, contract_ids, liquidacion.id, context=context)]
            #print lines
            self.write(cr, uid, [liquidacion.id], {'line_ids': lines}, context=context)
        return True
    
    def get_payslip_lines(self, cr, uid, contract_ids, payslip_id, context):
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
                            FROM hr_liquidation_compute as hp, hr_liquidation_input as pi \
                            WHERE hp.employee_id = %s AND hp.state = 'done' \
                            AND hp.date_from >= %s AND hp.date_to <= %s AND hp.id = pi.payslip_id AND pi.code = %s",
                           (self.employee_id, from_date, to_date, code))
                res = self.cr.fetchone()[0]
                return res or 0.0
            
        class WorkedDays(BrowsableObject):
            """a class that will be used into the python code, mainly for usability purposes"""
            def _sum(self, code, from_date, to_date=None):
                if to_date is None:
                    to_date = datetime.now().strftime('%Y-%m-%d')
                result = 0.0
                self.cr.execute("SELECT sum(number_of_days) as number_of_days, sum(number_of_hours) as number_of_hours\
                            FROM hr_payslip as hp, hr_payslip_worked_days as pi \
                            WHERE hp.employee_id = %s AND hp.state = 'done'\
                            AND hp.date_from >= %s AND hp.date_to <= %s AND hp.id = pi.payslip_id AND pi.code = %s",
                           (self.employee_id, from_date, to_date, code))
                return self.cr.fetchone()

            def sum(self, code, from_date, to_date=None):
                res = self._sum(code, from_date, to_date)
                return res and res[0] or 0.0

            def sum_hours(self, code, from_date, to_date=None):
                res = self._sum(code, from_date, to_date)
                return res and res[1] or 0.0

        class Payslips(BrowsableObject):
            """a class that will be used into the python code, mainly for usability purposes"""

            def sum(self, code, from_date, to_date=None):
                if to_date is None:
                    to_date = datetime.now().strftime('%Y-%m-%d')
                self.cr.execute("SELECT sum(case when hp.credit_note = False then (pl.total) else (-pl.total) end)\
                            FROM hr_payslip as hp, hr_payslip_line as pl \
                            WHERE hp.employee_id = %s AND hp.state = 'done' \
                            AND hp.date_from >= %s AND hp.date_to <= %s AND hp.id = pl.slip_id AND pl.code = %s",
                            (self.employee_id, from_date, to_date, code))
                res = self.cr.fetchone()
                return res and res[0] or 0.0

        #we keep a dict with the result because a value can be overwritten by another rule with the same code
        result_dict = {}
        rules = {}
        categories_dict = {}
        blacklist = []
        payslip_obj = self.pool.get('hr.liquidation.compute')
        #inputs_obj = self.pool.get('hr.payslip.worked_days')
        obj_rule = self.pool.get('hr.liquidation.rule')
        payslip = payslip_obj.browse(cr, uid, payslip_id, context=context)
        #worked_days = {}
        #for worked_days_line in payslip.worked_days_line_ids:
        #    worked_days[worked_days_line.code] = worked_days_line
        inputs = {}
        for input_line in payslip.input_line_ids:
            if inputs.has_key(input_line.code):
                inputs[input_line.code].amount +=  input_line.amount
            else:
                inputs[input_line.code] = input_line

        categories_obj = BrowsableObject(self.pool, cr, uid, payslip.contract_id.employee_id.id, categories_dict)
        input_obj = InputLine(self.pool, cr, uid, payslip.employee_id.id, inputs)
        #worked_days_obj = WorkedDays(self.pool, cr, uid, payslip.employee_id.id, worked_days)
        payslip_obj = Payslips(self.pool, cr, uid, payslip.contract_id.employee_id.id, payslip)
        rules_obj = BrowsableObject(self.pool, cr, uid, payslip.contract_id.employee_id.id, rules)
        
        #localdict = {'categories': categories_obj, 'rules': rules_obj, 'payslip': payslip_obj, 'worked_days': worked_days_obj, 'inputs': input_obj}
        
        #sri_ec_obj = sri_ec(self.pool, cr, uid, payslip.employee_id.id, payslip_obj)
        #localdict = {'categories': categories_obj, 'rules': rules_obj, 'payslip': payslip_obj, 'worked_days': worked_days_obj, 'inputs': input_obj, 'sri_ec': sri_ec_obj, 'date_time':fechas}
        localdict = {'categories': categories_obj, 'rules': rules_obj, 'liquidation': payslip_obj, 'easy_datetime': easy_datetime, 'inputs': input_obj}
        
        #AQUI SE OBTIENE LA ESTRUCTURA DEL CONTRATO
        structure_ids = [payslip.structure_id.id]
        #if context.has_key('otra_estructura'):
        #    #aplico la estructura indicada en el wizard
        #    if context['otra_estructura']!=False:
        #        structure_ids = [context['otra_estructura'][0]]
        #        #structure_ids = [contract.struct_id.id for contract in self.pool.get('hr.contract').browse(cr, uid, [context['otra_estructura'][0]], context=context)]
        #        structure_ids = list(set(self.pool.get('hr.liquidation.structure')._get_parent_structure(cr, uid, structure_ids, context=context)))
        #    else:
        #        structure_ids = self.pool.get('hr.contract').get_all_structures(cr, uid, contract_ids, context=context)
        #else:
        #    #get the ids of the structures on the contracts and their parent id as well
        #    structure_ids = self.pool.get('hr.contract').get_all_structures(cr, uid, contract_ids, context=context)
        #    #get the rules of the structure and thier children
        rule_ids = self.pool.get('hr.liquidation.structure').get_all_rules(cr, uid, structure_ids, context=context)
        #run the rules by sequence
        sorted_rule_ids = [id for id, sequence in sorted(rule_ids, key=lambda x:x[1])]

        for contract in self.pool.get('hr.contract').browse(cr, uid, contract_ids, context=context):
            employee = contract.employee_id
            localdict.update({'employee': employee, 'contract': contract})
            for rule in obj_rule.browse(cr, uid, sorted_rule_ids, context=context):
                key = rule.code + '-' + str(contract.id)
                localdict['result'] = None
                localdict['result_qty'] = 1.0
                #check if the rule can be applied
                if obj_rule.satisfy_condition(cr, uid, rule.id, localdict, context=context) and rule.id not in blacklist:
                    #compute the amount of the rule
                    amount, qty, rate = obj_rule.compute_rule(cr, uid, rule.id, localdict, context=context)
                    #print amount
                    #check if there is already a rule computed with that code
                    previous_amount = rule.code in localdict and localdict[rule.code] or 0.0
                    #set/overwrite the amount computed for this rule in the localdict
                    tot_rule = amount * qty * rate / 100.0
                    localdict[rule.code] = tot_rule
                    rules[rule.code] = rule
                    #sum the amount for its salary category
                    localdict = _sum_salary_rule_category(localdict, rule.category_id, tot_rule - previous_amount)
                    #create/overwrite the rule in the temporary results
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
                    }
                else:
                    #blacklist this rule and its children
                    blacklist += [id for id, seq in self.pool.get('hr.liquidation.rule')._recursive_search_of_rules(cr, uid, [rule], context=context)]

        result = [value for code, value in result_dict.items()]
        return result
    
hr_liquidation_compute()

class hr_liquidation_line(osv.osv):
    '''
    Liquidation Line
    '''

    _name = 'hr.liquidation.line'
    _inherit = 'hr.liquidation.rule'
    _description = 'Linea de Liquidación'
    _order = 'contract_id, sequence'

    def _calculate_total(self, cr, uid, ids, name, args, context):
        if not ids: return {}
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            res[line.id] = float(line.quantity) * line.amount * line.rate / 100
        return res

    _columns = {
        'liquidation_id':fields.many2one('hr.liquidation.compute', 'Liquidación', required=True, ondelete='cascade'),
        'salary_rule_id':fields.many2one('hr.liquidation.rule', 'Regla', required=True),
        'employee_id':fields.many2one('hr.employee', 'Empleado', required=True),
        'contract_id':fields.many2one('hr.contract', 'Contrato', required=True, select=True),
        'rate': fields.float('Porcentaje (%)', digits_compute=dp.get_precision('Payroll Rate')),
        'amount': fields.float('Monto', digits_compute=dp.get_precision('Payroll')),
        'quantity': fields.float('Cantidad', digits_compute=dp.get_precision('Payroll')),
        'total': fields.function(_calculate_total, method=True, type='float', string='Total', digits_compute=dp.get_precision('Payroll'),store=True ),
    }

    _defaults = {
        'quantity': 1.0,
        'rate': 100.0,
    }

hr_liquidation_line()
