
# -*- coding: utf-8 -*-
import base64

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

from odoo.modules import get_module_resource




class UniversityContract(models.Model):

    _name = 'university.contract'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Contrato"

    #Campos Char
    name = fields.Char(string="Reference No.", copy=False,
                       help="Secuencia del Documento",
                       default=lambda self: _('Nuevo'))

    #campos Realacionados
    pearson_id = fields.Many2one('university.pearson', string='Estudiante')
    pearson_id_career_rel  = fields.Many2many(related ='pearson_id.career', string='Carreras del Estudiante')
    season_id = fields.Many2one('university.academic.season', string='Periodo Academico')
    career_id = fields.Many2one('university.academic.career', string='Carrera')

    line_contract_ids = fields.One2many('university.contract.line', 'contrac_id', string='Lineas de contrato')
    


    #Campos tipo Fecha
    date = fields.Date(string='Fecha del documento')


    #Campos tipo Selection
    state = fields.Selection([('draft', 'Borrador'), ('done', 'Confirmado'), ('payed', 'Pagado')],string = "Estado",default="draft")

    payment_ids  = fields.Many2many('university.payment', string='Pagos')
    
    
    
    @api.depends("line_contract_ids","line_contract_ids.amount")
    def _compute_amount_total(self):
        for rec in self:
            total_amount = 0
            if rec.line_contract_ids:
                total_amount = sum(rec.line_contract_ids.mapped('amount'))       
            rec.amount_total = total_amount
    
    @api.depends("payment_ids","payment_ids.amount")
    def _compute_amount_total_residual(self):
        for rec in self:
            total_amount = rec.amount_total
            if rec.payment_ids:
                total_amount = sum(rec.payment_ids.mapped('amount'))       
                rec.amount_total_residual = rec.amount_total - total_amount 
            else:rec.amount_total_residual = rec.amount_total
            
    def get_residual(self):
        for rec in self:
            self._compute_amount_total()
            total_amount = rec.amount_total
            if rec.payment_ids:
                total_amount = sum(rec.payment_ids.mapped('amount'))       
            return rec.amount_total - total_amount 
        
             
    amount_total  = fields.Float(string='Monto Total', compute = "_compute_amount_total")
    amount_total_residual  = fields.Float(string='Total Pendiente', compute = "_compute_amount_total_residual")
    
    
    @api.onchange('pearson_id')
    def onchange_campo(self):
        # Lógica para calcular el dominio del campo
        domain = [('id', 'in', [line.id for line in self.pearson_id.career])]
        return {'domain': {'career_id': domain}}

    @api.model
    def create(self, vals):
        if vals.get('name', _('Nuevo')) == _('Nuevo'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'university.contract') or _('Nuevo')
        res = super(UniversityContract, self).create(vals)
        return res


    def action_validate(self):
        self.state = "done"
        
    def action_pay_document(self):
        return  {
                'name': "Registro de pago",
                'type': 'ir.actions.act_window',
                'res_model': 'university.payment',
                'view_mode': 'form',
                'view_type': 'form',
                'target': 'new',
            }

class UniversityContractLine(models.Model):

    _name = 'university.contract.line'
    _description = "Lineas del Contrato"

    contrac_id = fields.Many2one('university.contract', string='Contrato' )
    subject_id = fields.Many2one('university.subjects', string='Materia',required = True)
    pearson_id = fields.Many2one('university.pearson', string='Docente',required = True)
    time_sheet = fields.Many2one('university.subjects.teachers', string='Horario',required = True) 
    amount  = fields.Float(string='Monto')
    

    

