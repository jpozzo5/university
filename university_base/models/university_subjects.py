
# -*- coding: utf-8 -*-



import base64

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class UniversitySubjects(models.Model):

    _name = 'university.subjects'
    _description = "Materia Universitaria"

    #Campos Char
    name = fields.Char('Nombre', required=True)
    code = fields.Char(string='Código')

    career_ids  = fields.Many2many('university.academic.career', string='Carreras Academica',required=True)
    num_season = fields.Selection([(str(i), str(i)) for i in range(1, 21)],string = "Del Trimestre",required=True )
    

    @api.constrains('code')
    def _check_identify_uniqueness(self):
        for record in self:
            if (
                self.search([('code', '=', record.code)])
                - record
            ):
                raise ValidationError("La identificación debe ser única.")
    

    
 
    
