
# -*- coding: utf-8 -*-



import base64

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

import datetime

class UniversitySubjectsTeaches(models.Model):

    _name = 'university.subjects.teachers'
    _description = "Materia Universitaria"
    _rec_name= "pearson_id"

    
    pearson_id  = fields.Many2one('university.pearson', string='Docente',required = True)
    subject_id = fields.Many2one('university.subjects', string='Materia Academica',required = True)
    pearson_id_subject_id_rel = fields.Many2many(related="pearson_id.subjects_ids", string='Materias del Docente')

    from_time  = fields.Float(string='Desde',required = True)
    until_time = fields.Float(string='Hasta',required = True)


    
    def hora_string(self,field):
        if field:
            horas = int(field)  # Obtenemos la parte  del float
            minutos = round((field - int(field)) * 60)  # Obtenemos los minutos
            hora_formato_hora = datetime.time(horas, minutos)  # Convertimos a formato de hora
            return  hora_formato_hora.strftime('%H:%M')  # Convertimos la hora a formato de string
        else:
            return  ""

    day  = fields.Selection(
        [
            ('1', 'Lunes'), 
            ('2', 'Martes'),
            ('3', 'Miercoles'),
            ('4', 'Jueves'),
            ('5', 'Viernes'),
            ('6', 'Sabado'),
        ],
        string = "Día",
        default = "1",

    )
    
    def obtener_segundo_valor(self,field):   
        return dict(self._fields['day'].selection).get(field)


    @api.constrains('pearson_id', 'from_time', 'until_time')
    def _check_time_overlap(self):
        for rec in self:
            overlap_clases = self.search([
                ('id', '!=', rec.id),
                ('pearson_id', '=', rec.pearson_id.id),
                ('day', '=', rec.day),
                ('from_time', '<', rec.until_time),
                ('until_time', '>', rec.from_time)
            ])
            if overlap_clases:
                raise models.ValidationError('El horario se superpone con otra clase del mismo profesor')


    
    def name_get(self):
        return [(rec.id, f"{self.obtener_segundo_valor(rec.day)} {self.hora_string(rec.from_time)} / {self.hora_string(rec.until_time)} ") for rec in self]
    
    
    

    
 
    
