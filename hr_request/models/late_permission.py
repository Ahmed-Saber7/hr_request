# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, date, timedelta, time
from odoo.exceptions import UserError, AccessError, ValidationError
import pytz


class LatePermission(models.Model):
    _name = 'late.permission'
    _rec_name = 'name'
    _inherit = ['mail.thread']

    state = fields.Selection([
        ('draft', 'DRAFT'),
        ('direct_manager', 'DIRECT MANAGER'),
        ('hr_manager', 'HR MANAGER'),
        ('approved', 'APPROVED'),
        ('rejected', 'REJECTED'),
    ], string='Status', track_visibility='onchange', default='draft')

    @api.returns('self')
    def _default_employee_get(self):
        return self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)

    employee_id = fields.Many2one('hr.employee', string='Employee', readonly=True, default=_default_employee_get)
    direct_manager = fields.Many2one('res.users', related='employee_id.parent_id.user_id',
                                     string='Direct Manager')
    name = fields.Char(string=" ", required=False, readonly=True)
    description = fields.Text(string="Description", required=False, )
    date = fields.Date(string="Date", required=True, default=date.today())
    permission_time = fields.Datetime(string="Permission Time", required=True, default=datetime.today())

    @api.model
    def create(self, vals):
        vals['name'] = (self.env['ir.sequence'].next_by_code('late.permission')) or 'New'
        return super(LatePermission, self).create(vals)

    type = fields.Selection([
        ('late', 'Late Sign in'),
        ('early', 'Early Sign out'),
    ], string='Permission Type', required=True)

    @api.constrains('type')
    def _check_type_choosed_before(self):
        constant = 0
        if self.type == 'early':
            #TODO Get Values From Configration Screen
            config = self.env['res.config.settings'].search([])
            print("config  >>", config)
            max_of_early_late_permission = config.max_of_early_late_permission
            print("max_of_early_late_permission ##########", max_of_early_late_permission)
            max_of_early_late_permission_time = config.max_of_early_late_permission_time
            print("max_of_early_late_permission_time ##########", max_of_early_late_permission_time)

            # TODO check if the request time over than 13:30pm or not
            # TODO Convert Time From UTC to User TimeZone
            the_time = self.permission_time
            user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)
            time_in_timezone = pytz.utc.localize(the_time).astimezone(user_tz)
            print("Time in UTC -->", time_in_timezone)
            the_finall_time = datetime.strftime(time_in_timezone, "%H.%M")
            print("Time in Users Timezone -->", the_finall_time)
            the_finall_time_float = float(the_finall_time)
            print("the_finall_time_float >>>> ", the_finall_time_float)

            if the_finall_time_float > max_of_early_late_permission_time:
                print("yes its over")
                raise ValidationError(_('you cant create Early Sign out before 01.30 pm ..!'))

            # TODO check if the employee created Early Sign out more than two times in same month
            late_object = self.env['late.permission'].search(
                [('employee_id', '=', self.employee_id.id)])
            if late_object:
                print("late_object >>>> ", late_object)
                for late in late_object:
                    if late.type == 'early':
                        print("late_object date>>>> ", late.date)
                        print("late_object type>>>> ", late.type)
                        print("late_object date>>>> ", late.date.month)
                        current_month1 = late.date.month
                        current_month2 = self.date.month
                        print("current_month1 >>>>>", current_month1)
                        print("current_month2 >>>>>", current_month2)
                        if current_month1 == current_month2:
                            print("ahmed saber")
                            print("______________________________________________")
                            constant = constant + 1
        print("constant >>>>>", constant)
        if constant > max_of_early_late_permission:
            print("yes it working")
            raise ValidationError(_('you have already take this option Two times before this month ..!'))

    @api.multi
    def employee_confirm(self):
        for rec in self:
            rec.state = 'direct_manager'
            self._action_send_email()

    @api.multi
    def direct_manager_confirm(self):
        for rec in self:
            current_user = rec.env.user
            if not current_user == rec.direct_manager:
                raise ValidationError(_('You Cant Approve This Request'))
            else:
                rec.state = 'hr_manager'
                self._action_send_email()

    @api.multi
    def hr_manager_confirm(self):
        for rec in self:
            if not rec.env.user.has_group('hr.group_hr_manager'):
                raise ValidationError(_('You Cant Approve This Request'))
            else:
                rec.state = 'approved'
                self._action_send_email()

    @api.multi
    def reject(self):
        for rec in self:
            if rec.state == 'direct_manager':
                current_user = rec.env.user
                if not current_user == rec.direct_manager:
                    raise ValidationError(_('You Cant Reject This Request'))
                else:
                    rec.state = 'rejected'
                    self._action_send_email()
            elif rec.state == 'hr_manager':
                if not rec.env.user.has_group('hr.group_hr_manager'):
                    raise ValidationError(_('You Cant Reject This Request'))
                else:
                    rec.state = 'rejected'
                    self._action_send_email()

    def _action_send_email(self):
        action_id = self.env.ref('hr_request.action_late_permission').id
        base = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        base += "/web" + "/#id=%s&view_type=form&model=late.permission&action=%s" % (self.id, action_id)
        self.link = base
        template_id = self.env.ref('hr_request.mail_template_late_permission')

        if self.state == "direct_manager":
            for use in self:
                template_id.email_to = use.employee_id.work_email
                template_id.body_html = """
                <div style="margin: 10px auto; direction:rtl;">
                <p> احمد صابر السيد محمود</p>
                </div>
                """
            res = template_id.send_mail(use.id, force_send=True)
            print('***res', res)

        if self.state == "hr_manager":
            for use in self:
                template_id.email_to = use.employee_id.work_email
                template_id.body_html = """
                   <div style="margin: 10px auto; direction:rtl;">
                   <p> احمد صابر السيد محمود</p>
                   </div>
                   """
            res = template_id.send_mail(use.id, force_send=True)
            print('***res', res)

        if self.state == "approved":
            for use in self:
                template_id.email_to = use.employee_id.work_email
                template_id.body_html = """
                   <div style="margin: 10px auto; direction:rtl;">
                   <p> احمد صابر السيد محمود</p>
                   </div>
                   """
            res = template_id.send_mail(use.id, force_send=True)
            print('***res', res)

        if self.state == "rejected":
            for use in self:
                template_id.email_to = use.employee_id.work_email
                template_id.body_html = """
                   <div style="margin: 10px auto; direction:rtl;">
                   <p> احمد صابر السيد محمود</p>
                   </div>
                   """
            res = template_id.send_mail(use.id, force_send=True)
            print('***res', res)
