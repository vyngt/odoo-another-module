# -*- coding: utf-8 -*-
# from odoo import http


# class TutorialCheckout(http.Controller):
#     @http.route('/tutorial_checkout/tutorial_checkout', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tutorial_checkout/tutorial_checkout/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('tutorial_checkout.listing', {
#             'root': '/tutorial_checkout/tutorial_checkout',
#             'objects': http.request.env['tutorial_checkout.tutorial_checkout'].search([]),
#         })

#     @http.route('/tutorial_checkout/tutorial_checkout/objects/<model("tutorial_checkout.tutorial_checkout"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tutorial_checkout.object', {
#             'object': obj
#         })
