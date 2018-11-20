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

from openerp.tests.common import TransactionCase

class PartnerTest(TransactionCase):

    def setUp(self):
        super(PartnerTest, self).setUp()
        self.Partner = self.registry('res.partner')

    def test_create(self):
        cursor = self.cr
        user_id = self.uid
        partner_id = self.Partner.create(
            cursor,
            user_id,
            {
                'ced_ruc': '0103893962',
                'name': 'CRISTIAN GONZALO SALAMEA MALDONADO',
                'type_ced_ruc': 'cedula',
                'tipo_persona': '6'                
            }
        )
        self.assertNotEquals(partner_id, 0)

