
# -*- coding: utf-8 -*-



import base64

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

from odoo.modules import get_module_resource
from odoo.tools import config

from cryptography.fernet import Fernet
import hashlib

try:
    from odoo.tools import image_colorize
except Exception:
    image_colorize = False

class UniversityPearson(models.Model):

    _name = 'university.pearson'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Personas"

    #Campos Char
    name = fields.Char('Nombre ', required=True)
    identify = fields.Char(string='Identificación', required=True)
    street = fields.Char(string='Dirección Completa')
    phone  = fields.Char(string='Número de Contacto')
    email  = fields.Char(string='Correo Eletrónico') 
    card_code  = fields.Char(string='N° Carnet')
    dashboard_token  = fields.Char(string='Llave del esudiante')
    dashboard_token_url = fields.Char(string='URL Dashboard')

    #campos Selections
    pearson_type = fields.Selection(
            [('teacher', 'Docente'), ('student', 'Estudiante'),],
            'Tipo de Persona',
            default ="student"
        )
    

    #campos tipo fecha
    birthdate  = fields.Date(string = 'Fecha de nacimiento')
    
    #Campos Relacionados
    career = fields.Many2many('university.academic.career', string='Carrera Academica')
    subjects_ids = fields.Many2many('university.subjects', string='Materias')
    time_sheet_ids = fields.One2many('university.subjects.teachers','pearson_id', string = 'Horario')

    
    


    #CAmpos Binarios  

    @api.model
    def _default_image(self):
        """Method to get default Image"""
        image_path = get_module_resource(
            "hr", "static/src/img", "default_image.png"
        )
        return base64.b64encode(open(image_path, "rb").read())

    photo = fields.Binary(
        "Photo", default=_default_image, help="Attach student photo"
    )
    


    """
        Hace que el numero de indentificacion sea único 
    """
    @api.constrains('identify')
    def _check_identify_uniqueness(self):
        for record in self:
            if (
                self.search([('identify', '=', record.identify)])
                - record
            ):
                raise ValidationError("La identificación debe ser única.")
    

    

        
    @api.model
    def create(self, vals):
        res = super(UniversityPearson, self).create(vals)
        if res.pearson_type == 'student':
            token = hashlib.md5(str(res.id).encode()).hexdigest()
            url  = self.env['ir.config_parameter'].get_param('web.base.url')
            res.dashboard_token = token
            res.dashboard_token_url = f"{url}/dashboard?viewr={token}" 
        return res