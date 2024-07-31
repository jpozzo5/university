
# -*- coding: utf-8 -*-



import base64

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class UniversityAcademicCareer(models.Model):

    _name = 'university.academic.career'
    _description = "Carrera"


    name = fields.Char(
            'Carrera Academica', 
            required=True
        )

    type = fields.Selection(
            [
                ('tsu', 'Técnico Superios'), 
                ('lc', 'Licenciatura'),
                ('ing', 'Ingenieria'),
  
            ]
            ,
            required=True ,
            string ="Tipo de carrera",
            default = "tsu"
        )

   
    

    def name_get(self):
        return [(rec.id, f"{rec.type} {rec.name} ") for rec in self]


