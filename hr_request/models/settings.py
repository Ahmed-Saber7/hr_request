# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from ast import literal_eval


class HRSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    max_of_early_late_permission = fields.Integer(string="Default Maximum Of Early Sign out", required=False, )
    max_of_early_late_permission_time = fields.Float(string="Default Maximum Of Early Sign out Time", required=False, )

    num_months = fields.Integer('Pre Ending Date Months To Notify')
    trial_num_months = fields.Integer('Pre Trial Ending Date Months To Notify')

    def set_values(self):
        res = super(HRSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('hr_request.max_of_early_late_permission',
                                                  self.max_of_early_late_permission)

        self.env['ir.config_parameter'].set_param('hr_request.max_of_early_late_permission_time',
                                                  self.max_of_early_late_permission_time)

        self.env['ir.config_parameter'].set_param('hr_request.num_months',
                                                  self.num_months)

        self.env['ir.config_parameter'].set_param('hr_request.trial_num_months',
                                                  self.trial_num_months)
        return res

    @api.model
    def get_values(self):
        res = super(HRSettings, self).get_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()

        max_of_early_late_permissions = ICPSudo.get_param('hr_request.max_of_early_late_permission')
        max_of_early_late_permissionss = int(max_of_early_late_permissions)

        max_of_early_late_permission_times = ICPSudo.get_param('hr_request.max_of_early_late_permission_time')
        max_of_early_late_permission_timess = float(max_of_early_late_permission_times)

        num_monthss = ICPSudo.get_param('hr_request.num_months')
        num_monthsss = int(num_monthss)

        trial_num_monthss = ICPSudo.get_param('hr_request.trial_num_months')
        trial_num_monthsss = int(trial_num_monthss)

        res.update(
            max_of_early_late_permission=max_of_early_late_permissionss,
            max_of_early_late_permission_time=max_of_early_late_permission_timess,

            num_months=num_monthsss,
            trial_num_months=trial_num_monthsss,

        )
        return res
