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
{
    'name': 'Talento Humano - Ecuador',
    'category': 'Localization/Payroll',
    'author': 'Carlos Andrés Ordóñez P.',
    'depends': ['hr_payroll', 'l10n_ec_tools', 'l10n_ec_partner'],
    'version': '1.0',
    'description': """
Talento Humano para Ecuador
=====================

    - Empleados con 2 nombres y 2 apellidos
    - Cédula como nombre de empleado
    - Cargas familiares, permitiendo descuentos de la Función Judicial
    - Aplicación del impuesto a la renta, fórmula en rol de pagos, como deducciones de gastos personales
    - Ingresos y Egresos adicionales
    - Fórmula de aportes al IESS
    - Fórmula de fondos de reserva

    """,

    'active': False,
    'data': [
        'security/l10n_ec_hr_security.xml',
        'security/ir.model.access.csv',
        'data/l10n_ec_res_partner_bank.xml',
        'data/l10n_ec_hr_misc_data.xml',
        'data/l10n_ec_hr_contract_data.xml',
        'data/l10n_ec_hr_holidays_data.xml',
        'data/l10n_ec_hr_payroll_data.xml',
        'data/payslip_template.xml',
        'l10n_ec_hr_view.xml',
        'l10n_ec_res_country_view.xml',
        'l10n_ec_hr_income_tax_view.xml',
        'l10n_ec_hr_employee_view.xml',
        'l10n_ec_hr_contract_view.xml',
        'l10n_ec_hr_holidays_view.xml',
        'l10n_ec_hr_io_view.xml',
        'l10n_ec_hr_he_view.xml',
        'l10n_ec_desvinculation_view.xml',
        'l10n_ec_hr_aspirante_view.xml',
        'l10n_ec_hr_payroll_view.xml',
        'wizard/l10n_ec_hr_payroll_payslips_by_employees_view.xml',
        'wizard/l10n_ec_hr_io_import_xls_view.xml',
        'wizard/l10n_ec_import_employee_projection_view.xml',
        #'wizard/archivo_banco_austro_view.xml',
        #'wizard/archivo_banco_internacional_view.xml',
        'wizard/archivo_bancos_view.xml',
        'wizard/archivo_iess_view.xml',
        'wizard/archivo_xiv_view.xml',
        'wizard/modificar_salario_view.xml',
        'wizard/exportar_asiento_view.xml',
        'wizard/exportar_provisiones_view.xml',
        'wizard/compers_employee_family_view.xml',
        'report/report.xml',
        'report/formato_vacaciones.xml',
        'report/rol_individual.xml',
        'l10n_ec_hr_cron.xml',
    ],
    'installable': True
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
