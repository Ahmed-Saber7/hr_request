# -*- coding: utf-8 -*-

from odoo import models, fields, api

from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta


class HrContract(models.Model):
    _inherit = 'hr.contract'

    pre_2mon_date = fields.Date(compute='compute_pre_2mon_date')
    pre_1mon_date = fields.Date(compute='compute_pre_2mon_date')
    link = fields.Char()

    def compute_pre_2mon_date(self):
        config = self.env['res.config.settings'].search([])
        self.pre_2mon_date = self.date_end - relativedelta(months=config.num_months)
        self.pre_1mon_date = self.trail_date_end - relativedelta(months=config.trial_num_months)

    @api.model
    def _cron_contract_ending(self):
        print('in')
        today_date = fields.Date.today()
        print('today is: ', today_date)
        matched_contracts = self.search(
            [('date_end', '>=', today_date), ('pre_2mon_date', '<=', today_date), ('active', '=', True)])
        print(matched_contracts)
        for contract in matched_contracts:
            template_id = contract.env.ref('hr_request.mail_template_ending_contract_notify')
            action = contract.env.ref('hr_contract.action_hr_contract').id
            template_id.email_from = contract.company_id.email
            group_hr_officers = contract.env.ref(
                'hr.group_hr_user').users
            for user in group_hr_officers:
                next_employee = contract.env['hr.employee'].search([('user_id', '=', user.id)], limit=1)
                if next_employee:
                    template_id.email_to = next_employee.work_email
                    print(user.lang)
                    if user.lang == 'ar_AA':
                        template_id.body_html = """
                            <div style="margin: 10px auto;direction:rtl;">
                               <div>
                            </div>
                               <p>  السيد/ {name} </p>
                               <p>

                                    """.format(name=next_employee.name) + """
                                    من فضلك قم بتحديث عقد الموظف <a href="${object.employee_id.name}"/>
                                    <a href="${object.link}">من هنا</a>
                                </p>
                            </div>
                         """
                    else:
                        template_id.body_html = """
                            <div style="margin: 10px auto;direction:rtl;">
                               <div>
                            </div>
                               <p> MR/ {name} </p>
                               <p>
                                    """.format(name=next_employee.name) + """
                                    Please renew contract for employee <a href="${object.employee_id.name}"/>
                                    <a href="${object.link}">From Here</a>
                                </p>
                            </div>
                        """
                    base = contract.env['ir.config_parameter'].sudo().get_param('web.base.url')
                    base += "/web" + "/#id=%s&view_type=form&model=hr.contract&action=%s" % (contract.id, action)
                    contract.link = base
                    res = template_id.send_mail(contract.id, force_send=True)
                    print('***re`s', res)

    @api.model
    def _cron_contract_trial_ending(self):
        print('in')
        today_date = fields.Date.today()
        print('today is: ', today_date)
        matched_contracts = self.search(
            [('trial_date_end', '>=', today_date), ('pre_1mon_date', '<=', today_date), ('active', '=', True)])
        print(matched_contracts)
        for contract in matched_contracts:
            template_id = contract.env.ref('hr_request.mail_template_trial_ending_contract_notify')
            action = contract.env.ref('hr_contract.action_hr_contract').id
            template_id.email_from = contract.company_id.email
            group_hr_officers = contract.env.ref(
                'hr.group_hr_user').users
            for user in group_hr_officers:
                next_employee = contract.env['hr.employee'].search([('user_id', '=', user.id)], limit=1)
                if next_employee:
                    template_id.email_to = next_employee.work_email
                    print(user.lang)
                    if user.lang == 'ar_AA':
                        template_id.body_html = """
                            <div style="margin: 10px auto;direction:rtl;">
                               <div>
                            </div>
                               <p>  السيد/ {name} </p>
                               <p>

                                    """.format(name=next_employee.name) + """
                                    لقد شارفت المده التجريبيه للموظف يرجى أخذ إجراء للعقد <a href="${object.employee_id.name}"/>
                                    <a href="${object.link}">من هنا</a>
                                </p>
                            </div>
                         """
                    else:
                        template_id.body_html = """
                            <div style="margin: 10px auto;direction:rtl;">
                               <div>
                            </div>
                               <p> MR/ {name} </p>
                               <p>
                                    """.format(name=next_employee.name) + """The trial end date for employee <a 
                                    href="${object.employee_id.name}"/> comes soon so please tack action <a href="${
                                    object.link}">From Here</a> </p> </div> """
                    base = contract.env['ir.config_parameter'].sudo().get_param('web.base.url')
                    base += "/web" + "/#id=%s&view_type=form&model=hr.contract&action=%s" % (contract.id, action)
                    contract.link = base
                    res = template_id.send_mail(contract.id, force_send=True)
                    print('***re`s', res)
