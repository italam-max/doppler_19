# -*- coding: utf-8 -*-
# from odoo import http


# class AlmxStock(http.Controller):
#     @http.route('/almx_stock/almx_stock', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/almx_stock/almx_stock/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('almx_stock.listing', {
#             'root': '/almx_stock/almx_stock',
#             'objects': http.request.env['almx_stock.almx_stock'].search([]),
#         })

#     @http.route('/almx_stock/almx_stock/objects/<model("almx_stock.almx_stock"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('almx_stock.object', {
#             'object': obj
#         })
