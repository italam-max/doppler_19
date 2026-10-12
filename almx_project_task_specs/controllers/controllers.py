# from odoo import http


# class AlmxProjectTaskSpecs(http.Controller):
#     @http.route('/almx_project_task_specs/almx_project_task_specs', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/almx_project_task_specs/almx_project_task_specs/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('almx_project_task_specs.listing', {
#             'root': '/almx_project_task_specs/almx_project_task_specs',
#             'objects': http.request.env['almx_project_task_specs.almx_project_task_specs'].search([]),
#         })

#     @http.route('/almx_project_task_specs/almx_project_task_specs/objects/<model("almx_project_task_specs.almx_project_task_specs"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('almx_project_task_specs.object', {
#             'object': obj
#         })

