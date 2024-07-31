# -*- coding: utf-8 -*-

{
    'name': 'Sistema Administrativo Universitario',
    'version': '16.0.1.0.0',
    'category': 'Universidad',
    'summary': """""",
    'description': """Control de Matriculas estudiantil""",
    'author': 'Jesus Pozzo',
    'website': '',
    'depends': ['base', 'portal', 'web'],
    'data': [
        #DATA
        'data/ir_sequence_data.xml',
        #Seguridad
        'security/school_security.xml',
        'security/ir.model.access.csv',
        #Vistas 
        "views/university_pearson.xml",
        "views/university_subjects.xml",
        "views/university_academic_season.xml",
        "views/university_academic_career.xml",
        "views/university_subjects_teaches.xml",
        "views/university_contract.xml",
        "views/menu.xml",
        #Wizards
        "wizard/university_payment.xml",
        #templates
        "views/templates.xml",

        #Resportes
       
    ],
    'demo': [],
    'assets': {
        'web.assets_backend': [
            "university_base/static/src/scss/dashboard.scss",
        ],
    },
    'images': [],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
