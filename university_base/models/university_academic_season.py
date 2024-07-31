
# -*- coding: utf-8 -*-



import base64

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class UniversityAcademicSeason(models.Model):

    _name = 'university.academic.season'
    _description = "Periodo Educativo"


    name = fields.Char(
            'Año Educativo', 
            required=True
        )

    season = fields.Selection(
            [
                ('1', '1mer Trimestre'), 
                ('2', '2do Trimestre'),
                ('3', '3er Trimestre'),
                ('4', '4to Trimestre')
            ]
            ,
            required=True ,
            string ="Trimestre",
            default = "1"
        )

    def name_get(self):
        return [(rec.id, f"{rec.name} / {rec.season}") for rec in self]


