# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import date
from odoo.exceptions import UserError, AccessError, ValidationError


class Disclaimer(models.Model):
    _name = 'disclaimer.request'
    _rec_name = 'name'
    _inherit = ['mail.thread']

    state = fields.Selection([
        ('hr_officer', 'HR OFFICER'),
        ('direct_manager', 'DIRECT MANAGER'),
        ('department_manager', 'DEPARTMENT MANAGER'),
        ('it_manager', 'IT MANAGER'),
        ('administrative_manager', 'ADMINISTRATIVE MANAGER'),
        ('hr_manager', 'HR MANAGER'),
        ('approved', 'APPROVED'),
        ('rejected', 'REJECTED'),
    ], string='Status', track_visibility='onchange', default='hr_officer')

    name = fields.Char(string="Name", required=False, readonly=True)
    date = fields.Date(string="Date", required=True, default=date.today())
    description = fields.Text(string="Description", required=False, )
    employee_id = fields.Many2one('hr.employee', string='Employee')

    direct_manager = fields.Many2one('res.users', related='employee_id.parent_id.user_id',
                                     string='Direct Manager')

    department_manager = fields.Many2one('res.users', related='employee_id.parent_id.user_id',
                                     string='Direct Manager')

    # department_manager = fields.Many2one('res.users', string="Department",
    #                                      related="employee_id.department_id.manager_id.user_id",
    #                                      readonly=True, store=True)

    @api.model
    def create(self, vals):
        vals['name'] = (self.env['ir.sequence'].next_by_code('disclaimer.request')) or 'New'
        return super(Disclaimer, self).create(vals)

    @api.multi
    def hr_officer_confirm(self):
        for rec in self:
            if rec.state == 'hr_officer':
                if not rec.env.user.has_group('hr.group_hr_user'):
                    raise ValidationError(_('You Cant Approve This Request'))
                else:
                    rec.state = 'direct_manager'
                    self._action_send_email()

    @api.multi
    def direct_manager_confirm(self):
        for rec in self:
            if rec.state == 'direct_manager':
                current_user = rec.env.user
                if not current_user == rec.direct_manager:
                    raise ValidationError(_('You Cant Approve This Request'))
                else:
                    rec.state = 'department_manager'
                    self._action_send_email()

    @api.multi
    def department_manager_confirm(self):
        for rec in self:
            if rec.state == 'department_manager':
                current_user = rec.env.user
                if not current_user == rec.department_manager:
                    raise ValidationError(_('You Cant Approve This Request'))
                else:
                    rec.state = 'it_manager'
                    self._action_send_email()

    @api.multi
    def it_manager_confirm(self):
        for rec in self:
            if rec.state == 'it_manager':
                if not rec.env.user.has_group('group_it_dept_manager'):
                    raise ValidationError(_('You Cant Approve This Request'))
                else:
                    rec.state = 'administrative_manager'
                    self._action_send_email()

    @api.multi
    def administrative_manager_confirm(self):
        for rec in self:
            if rec.state == 'it_manager':
                if not rec.env.user.has_group('group_administrative_manager'):
                    raise ValidationError(_('You Cant Approve This Request'))
                else:
                    rec.state = 'hr_manager'
                    self._action_send_email()

    @api.multi
    def hr_manager_confirm(self):
        for rec in self:
            if rec.state == 'hr_manager':
                if not rec.env.user.has_group('hr.group_hr_user'):
                    raise ValidationError(_('You Cant Approve This Request'))
                else:
                    rec.state = 'approved'
                    self._action_send_email()

    @api.multi
    def reject(self):
        for rec in self:
            if rec.state == 'hr_officer':
                if not rec.env.user.has_group('hr.group_hr_manager'):
                    raise ValidationError(_('You Cant Reject This Request'))
                else:
                    rec.state = 'rejected'
                    self._action_send_email()

            elif rec.state == 'direct_manager':
                current_user = rec.env.user
                if not current_user == rec.direct_manager:
                    raise ValidationError(_('You Cant Reject This Request'))
                else:
                    rec.state = 'rejected'
                    self._action_send_email()

            elif rec.state == 'department_manager':
                current_user = rec.env.user
                if not current_user == rec.department_manager:
                    raise ValidationError(_('You Cant Reject This Request'))
                else:
                    rec.state = 'rejected'
                    self._action_send_email()

            elif rec.state == 'it_manager':
                if not rec.env.user.has_group('group_it_dept_manager'):
                    raise ValidationError(_('You Cant Reject This Request'))
                else:
                    rec.state = 'rejected'
                    self._action_send_email()

            elif rec.state == 'administrative_manager':
                if not rec.env.user.has_group('group_administrative_manager'):
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
        action_id = self.env.ref('hr_request.action_disclaimer_request').id
        base = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        base += "/web" + "/#id=%s&view_type=form&model=disclaimer_request&action=%s" % (self.id, action_id)
        self.link = base
        template_id = self.env.ref('hr_request.mail_template_disclaimer_request')

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

        if self.state == "department_manager":
            for use in self:
                template_id.email_to = use.employee_id.work_email
                template_id.body_html = """
                <div style="margin: 10px auto; direction:rtl;">
                <p> احمد صابر السيد محمود</p>
                </div>
                """
            res = template_id.send_mail(use.id, force_send=True)
            print('***res', res)

        if self.state == "it_manager":
            for use in self:
                template_id.email_to = use.employee_id.work_email
                template_id.body_html = """
                <div style="margin: 10px auto; direction:rtl;">
                <p> احمد صابر السيد محمود</p>
                </div>
                """
            res = template_id.send_mail(use.id, force_send=True)
            print('***res', res)

        if self.state == "administrative_manager":
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
