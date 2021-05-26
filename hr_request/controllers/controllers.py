# -*- coding: utf-8 -*-
from odoo import http

# class HrRequest(http.Controller):
#     @http.route('/hr_request/hr_request/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hr_request/hr_request/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hr_request.listing', {
#             'root': '/hr_request/hr_request',
#             'objects': http.request.env['hr_request.hr_request'].search([]),
#         })

#     @http.route('/hr_request/hr_request/objects/<model("hr_request.hr_request"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hr_request.object', {
#             'object': obj
#         })