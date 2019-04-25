# -*- coding: utf-8 -*-

{
    'name': "Job Estimate Template",
    'version': '10.0.2',
    'category': 'sale',
    'website': 'www.hashmicro.com',
    'summary': 'Job Estimate Template',
    'description': """
        This is the Job Estimate Template master
        """,
    'author': 'Hashmicro / Jeel',
    'license': 'AGPL-3',
    "depends": ['sale', 'job_costing_management_extension'],
    'data': [
        'wizard/import_job_estimate_template.xml',
        'views/job_estimate_template_view.xml',
        'views/sale_estimate_job_view.xml',
    ],
    'installable': True,
    'application': True,
}