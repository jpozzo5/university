
from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.home import Home

import logging

class University(Home):
    @http.route('/dashboard', type='http', auth='none')
    def custom_route(self, **kwargs):
        # Tu lógica personalizada aquí
        token = kwargs.get('viewr',False)
        if not token:
            return http.Response(
                "Falta el token en la URL de solicitud. Proporcione un token válido..", 
                status=400
            )
            
        partner = request.env['university.pearson'].sudo().search([('dashboard_token', '=', token)])
        if not partner:
            return http.Response(
                "Falta el token en la URL de solicitud. Proporcione un token válido..", 
                status=400
            )
        contracts_ids = request.env['university.contract'].sudo().search([('pearson_id', '=', partner.id)])
        totalTesidual = sum([rec.amount_total_residual for rec in contracts_ids])
        totalContratsAmoun = sum([rec.amount_total for rec in contracts_ids])
        return http.request.render('university_base.dashboard_student', {
            'name':partner.name,
            'identify':partner.identify,
            'street':partner.street,
            'phone':partner.phone,
            'email':partner.email,
            'card_code':partner.card_code,
            'contracts_total': request.env['university.contract'].sudo().search_count([('pearson_id', '=', partner.id)]),
            'contracts_total_residual': totalTesidual,
            'totalContratsAmoun':totalContratsAmoun,
            'contracts_ids':contracts_ids
       
            
            
        })