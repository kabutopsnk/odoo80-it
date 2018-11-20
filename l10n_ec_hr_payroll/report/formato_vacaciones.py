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
from openerp.report import report_sxw
from openerp.osv import osv

class formato_vacaciones(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(formato_vacaciones, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'cr':cr,
            'uid': uid,
        })
        
class wrapped_formato_vacaciones(osv.AbstractModel):
    _name = 'report.l10n_ec_hr_payroll.formato_vacaciones'
    _inherit = 'report.abstract_report'
    _template = 'l10n_ec_hr_payroll.formato_vacaciones'
    _wrapped_report_class = formato_vacaciones


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
