
# -*- coding: utf-8 -*-
import base64

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

from odoo.modules import get_module_resource




class UniversityPayment(models.Model):

    _name = 'university.payment'
    _description = "Pagos"


    name = fields.Char(string="Reference No.", copy=False,
                       help="Secuencia del Documento",
                       default=lambda self: _('Nuevo'))

    ref  = fields.Char(string='Referencia')
    
    contract_id = fields.Many2one('university.contract', string='Contrato',required=True)
    amount  = fields.Float(string='Monto')

    @api.depends("contract_id","contract_id.payment_ids")
    def _compute_amount_residual(self):
        for rec in self:
            total_amount = rec.contract_id.amount_total
            importes = 0
            if rec.contract_id.payment_ids:
                importes = sum(rec.contract_id.payment_ids.mapped('amount'))       
            rec.residual = total_amount - importes
              
    residual = fields.Float(string='Saldo Deudor' ,  store=True, compute = "_compute_amount_residual")
    
    date = fields.Date(string='Fecha del pago',required=True)
    state = fields.Selection([('draft', 'Borrador'), ('done', 'Confirmado')],string = "Estado",default="draft")
    
    

        
        
    @api.model
    def create(self, vals):
        if vals.get('name', _('Nuevo')) == _('Nuevo'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'university.payment') or _('Nuevo')
        res = super(UniversityPayment, self).create(vals)
        return res
    
    def action_validate(self):
        for rec in self:
            if rec.amount <=0:
                raise ValidationError("El monto no debe ser negativo.")  
            if  rec.amount > rec.residual:
                raise ValidationError("El monto no debe ser superior al saldo pendiente.") 
                
            if rec.contract_id:
                rec.contract_id.payment_ids = [(4, rec.id)]
                rec.state = "done"
                rec.contract_id.message_post(body=f"Pago Realizado con un importe de  {rec.amount} con referencia {rec.ref} .") 
                if  sum(rec.contract_id.payment_ids.mapped('amount')) -  rec.contract_id.amount_total == 0:
                    rec.contract_id.state = "payed"
            return True
