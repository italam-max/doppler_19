# -*- coding: utf-8 -*-
# from odoo import http


# class AlmxSale(http.Controller):
#     @http.route('/almx_sale/almx_sale', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/almx_sale/almx_sale/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('almx_sale.listing', {
#             'root': '/almx_sale/almx_sale',
#             'objects': http.request.env['almx_sale.almx_sale'].search([]),
#         })

#     @http.route('/almx_sale/almx_sale/objects/<model("almx_sale.almx_sale"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('almx_sale.object', {
#             'object': obj
#         })
