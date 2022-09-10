# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2018-today Ascetic Business Solution <www.asceticbs.com>
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
#################################################################################
from odoo import api,fields,models,_
import odoo.addons.decimal_precision as dp
from datetime import date

#inherit AccountInvoice class. 
class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    penalty_source_invoice = fields.Char('Penalty Source Invoice')
    penalty = fields.Selection([('fixed', 'Penalty Amount'), ('penalty_percentage', 'Penalty Percentage'),],string='Penalty')
    percentage_of_penalty = fields.Float("Penalty Percentage",digits=dp.get_precision('Account'), default=0.0)
    fixed_amount = fields.Float("Penalty Amount",default=0.0)
    
    #create function for late payment penalty. 
    def late_payment_penalty(self):
        invoice_dict = {} 
        invoice_line_dict ={} 
        today_date = date.today()  
        current_date = str(today_date)
        product = self.env.ref('abs_late_payment_penalty.penalty_product')
        account_invoice_object = self.env['account.invoice']
        account_invoice_line_object = self.env['account.invoice.line']
        invoice_ids = self.env['account.invoice'].search([('state', '=', 'open')])
        if invoice_ids: 
            for invoice_id in invoice_ids:
                if invoice_id:  
                    if invoice_id.date_due == False:
                        continue 
                    elif invoice_id.date_due < current_date:
                        invoice_dict = {
                                        'partner_id':invoice_id.partner_id.id,
                                        'date_invoice':today_date, 
                                        'penalty_source_invoice':invoice_id.number
                                       }
                        if invoice_dict:    
                            invoice = account_invoice_object.create(invoice_dict)  
                        if invoice_id.penalty == 'fixed':  
                            invoice_line_dict = {
                                                 'invoice_id':invoice.id,
                                                 'product_id':product.id,
                                                 'price_unit':invoice_id.fixed_amount,
                                                 'account_id':invoice_id.partner_id.property_account_receivable_id.id, 
                                                 'name':'Penalty',
                                                }
                            if invoice_line_dict:
                                account_invoice_line_object.create(invoice_line_dict) 
                        elif invoice_id.penalty == 'penalty_percentage':  
                            penalty_cal_percentage = (invoice_id.residual * invoice_id.percentage_of_penalty) / 100 
                            invoice_line_dict = {
                                                 'invoice_id':invoice.id,
                                                 'product_id':product.id,
                                                 'price_unit':penalty_cal_percentage,
                                                 'account_id':invoice_id.partner_id.property_account_receivable_id.id, 
                                                 'name':'Penalty',
                                                }
                            if invoice_line_dict: 
                                account_invoice_line_object.create(invoice_line_dict)
