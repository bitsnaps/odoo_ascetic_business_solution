# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2018 Ascetic Business Solution <www.asceticbs.com>
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

from odoo import api, fields, models,_
import datetime

class Employee(models.Model):
    _inherit = 'hr.employee'

    working_week = fields.Float(string="Total Working Hours In Week",compute="count_employee_working_hours_in_current_week")
    working_month = fields.Float(string="Total Working Hours In Month",compute="count_employee_working_hours_in_current_month")

    #For computation of the employee's total working hours of current month:-
    def count_employee_working_hours_in_current_month(self):
        for recordset in self:
            todayDate = datetime.date.today()
            starting_date_of_month = todayDate.replace(day=1)
            ending_date_of_month = starting_date_of_month + datetime.timedelta(days=todayDate.day - 1)
            analytic_ids = self.env['account.analytic.line'].search([('user_id','=',recordset.user_id.id),('date','>=',starting_date_of_month),('date','<=',ending_date_of_month)])
            working_month = 0
            for line in analytic_ids:
                working_month = line.unit_amount + working_month 
                recordset.working_month = working_month

    #For computation of the employee's total working hours of current week:-
    def count_employee_working_hours_in_current_week(self):
        for recordset in self:
            today = datetime.datetime.today()
            starting_date_of_week = today - datetime.timedelta(days=today.weekday())
            ending_date_of_week = starting_date_of_week + datetime.timedelta(days=today.weekday())
            analytic_ids = self.env['account.analytic.line'].search([('user_id','=',recordset.user_id.id),('date','>=',starting_date_of_week),('date','<=',ending_date_of_week)]) 
            working_week = 0
            for line in analytic_ids:
                working_week = line.unit_amount +  working_week 
                recordset.working_week = working_week
                    

                    
