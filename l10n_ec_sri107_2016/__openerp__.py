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
    'name': 'SRI - 2016 - Formulario 107',
    'version': '1.0',
    'category': 'Human Resources',
    'description': """
SRI Ecuador
=====================

    - Formulario 107
    - RDEP

     """,
    'author': 'Carlos Andrés Ordóñez P.',
    'depends': ['l10n_ec_hr_payroll'],

    'data': ['data/secuencias.xml',
             'sri107_view.xml',
             'security/ir.model.access.csv',
    ],
    'installable': True,
    'active': False,
}
