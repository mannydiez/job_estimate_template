# -*- coding: utf-8 -*-
from odoo import api, models, fields, _
from odoo.exceptions import UserError
import odoo.addons.decimal_precision as dp
import xlwt
import base64
from StringIO import StringIO


class JobEstimateTemplate(models.Model):
    _name = 'job.estimate.template'

    name = fields.Char(string="Name", required=True, help="This field show the name of the job estimate template")
    uom = fields.Many2one('product.uom', string="UoM", required=True, help="This field shows the unit of measure")
    var_internal_ref = fields.Char(string="Internal Reference",
                                   required=True,
                                   help="This will be a second ID for Variable, so this should be unique")
    company_id = fields.Many2one(
        'res.company',
        required=True,
        default=lambda self: self.env.user.company_id,
        string='Company',
    )
    job_estimate_ids = fields.One2many('job.estimate.template.line', 'job_estimate_id')
    labour_estimate_ids = fields.One2many('job.estimate.template.line', 'labour_estimate_id')
    overhead_ids = fields.One2many('job.estimate.template.line', 'overhead_id')
    subcon_estimation_ids = fields.One2many('job.estimate.template.line', 'subcon_id')
    description = fields.Char('Description',help="This fields shows the description of the job estimate template")
    # Export template from Job Estimate Template with data in .xls file.
    @api.multi
    def export_xls_template(self):
        file_name = 'JobEstimateTemplate.xls'
        workbook = xlwt.Workbook(encoding="UTF-8")
        worksheet1 = workbook.add_sheet('Variable')
        worksheet2 = workbook.add_sheet('Material Estimation')
        worksheet3 = workbook.add_sheet('Labour Estimation')
        worksheet4 = workbook.add_sheet('Subcon Estimation')
        worksheet5 = workbook.add_sheet('Overhead Estimation')

        style = xlwt.easyxf('font:bold True, name Arial;align: horiz center;')

        worksheet1.write(0, 0, 'Variable ID', style)
        worksheet1.write(0, 1, 'Name', style)
        worksheet1.write(0, 2, 'UoM', style)
        worksheet1.write(1, 0, self.var_internal_ref)
        worksheet1.write(1, 1, self.name)
        worksheet1.write(1, 2, self.uom.id)

        worksheet2.write(0, 0, 'Variable ID', style)
        worksheet2.write(0, 1, 'Item ID', style)
        worksheet2.write(0, 2, 'Product', style)
        worksheet2.write(0, 3, 'Description', style)
        worksheet2.write(0, 4, 'Quantity', style)
        worksheet2.write(0, 5, 'Unit of Measure', style)
        worksheet2.write(0, 6, 'Unit Price', style)
        worksheet2.write(0, 7, 'Adjustment (%)', style)
        worksheet2.write(0, 8, 'Subtotal', style)

        worksheet3.write(0, 0, 'Variable ID', style)
        worksheet3.write(0, 1, 'Item ID', style)
        worksheet3.write(0, 2, 'Product', style)
        worksheet3.write(0, 3, 'Description', style)
        worksheet3.write(0, 4, 'Quantity', style)
        worksheet3.write(0, 5, 'UoM Quantity', style)
        worksheet3.write(0, 6, 'Unit of Measure', style)
        worksheet3.write(0, 7, 'Unit Price', style)
        worksheet3.write(0, 8, 'Adjustment (%)', style)
        worksheet3.write(0, 9, 'Subtotal', style)

        worksheet4.write(0, 0, 'Variable ID', style)
        worksheet4.write(0, 1, 'Item ID', style)
        worksheet4.write(0, 2, 'Product', style)
        worksheet4.write(0, 3, 'Description', style)
        worksheet4.write(0, 4, 'Quantity', style)
        worksheet4.write(0, 5, 'Unit of Measure', style)
        worksheet4.write(0, 6, 'Unit Price', style)
        worksheet4.write(0, 7, 'Adjustment (%)', style)
        worksheet4.write(0, 8, 'Subtotal', style)

        worksheet5.write(0, 0, 'Variable ID', style)
        worksheet5.write(0, 1, 'Item ID', style)
        worksheet5.write(0, 2, 'Product', style)
        worksheet5.write(0, 3, 'Description', style)
        worksheet5.write(0, 4, 'Quantity', style)
        worksheet5.write(0, 5, 'Unit of Measure', style)
        worksheet5.write(0, 6, 'Unit Price', style)
        worksheet5.write(0, 7, 'Adjustment (%)', style)
        worksheet5.write(0, 8, 'Subtotal', style)

        row = 1
        # estimations=[]
        for estm_line2 in self.job_estimate_ids:
            column = 0
            worksheet2.write(row, column, self.var_internal_ref)
            column += 1
            worksheet2.write(row, column, estm_line2.product_id.default_code or "")
            column += 1
            worksheet2.write(row, column, estm_line2.product_id.name)
            column += 1
            worksheet2.write(row, column, estm_line2.product_description)
            column += 1
            worksheet2.write(row, column, estm_line2.product_uom_qty)
            column += 1
            worksheet2.write(row, column, estm_line2.product_uom.name)
            column += 1
            worksheet2.write(row, column, estm_line2.price_unit)
            column += 1
            worksheet2.write(row, column, estm_line2.discount)
            column += 1
            worksheet2.write(row, 8, estm_line2.price_subtotal)
            row += 1

        row = 1
        for estm_line3 in self.labour_estimate_ids:
            column = 0
            worksheet3.write(row, column, self.var_internal_ref)
            column += 1
            worksheet3.write(row, column, estm_line3.product_id.default_code or "")
            column += 1
            worksheet3.write(row, column, estm_line3.product_id.name)
            column += 1
            worksheet3.write(row, column, estm_line3.product_description)
            column += 1
            worksheet3.write(row, column, estm_line3.product_uom_qty)
            column += 1
            worksheet3.write(row, column, estm_line3.uom_qty)
            column += 1
            worksheet3.write(row, column, estm_line3.product_uom.name)
            column += 1
            worksheet3.write(row, column, estm_line3.price_unit)
            column += 1
            worksheet3.write(row, column, estm_line3.discount)
            column += 1
            worksheet3.write(row, 9, estm_line3.price_subtotal)
            row += 1

        row = 1
        # estimations=[]
        for estm_line4 in self.subcon_estimation_ids:
            column = 0
            worksheet4.write(row, column, self.var_internal_ref)
            column += 1
            worksheet4.write(row, column, estm_line4.product_id.default_code or "")
            column += 1
            worksheet4.write(row, column, estm_line4.product_id.name)
            column += 1
            worksheet4.write(row, column, estm_line4.product_description)
            column += 1
            worksheet4.write(row, column, estm_line4.product_uom_qty)
            column += 1
            worksheet4.write(row, column, estm_line4.product_uom.name)
            column += 1
            worksheet4.write(row, column, estm_line4.price_unit)
            column += 1
            worksheet4.write(row, column, estm_line4.discount)
            column += 1
            worksheet4.write(row, 8, estm_line4.price_subtotal)
            row += 1

        row = 1
        # estimations=[]
        for estm_line5 in self.overhead_ids:
            column = 0
            worksheet5.write(row, column, self.var_internal_ref)
            column += 1
            worksheet5.write(row, column, estm_line5.product_id.default_code or "")
            column += 1
            worksheet5.write(row, column, estm_line5.product_id.name)
            column += 1
            worksheet5.write(row, column, estm_line5.product_description)
            column += 1
            worksheet5.write(row, column, estm_line5.product_uom_qty)
            column += 1
            worksheet5.write(row, column, estm_line5.product_uom.name)
            column += 1
            worksheet5.write(row, column, estm_line5.price_unit)
            column += 1
            worksheet5.write(row, column, estm_line5.discount)
            column += 1
            worksheet5.write(row, 8, estm_line5.price_subtotal)
            row += 1

        fp = StringIO()
        workbook.save(fp)
        export_xls = self.env['download.excel.report'].create(
            {'excel_file': base64.encodestring(fp.getvalue()), 'file_name': file_name})
        fp.close()
        return {
            'view_mode': 'form',
            'res_id': export_xls.id,
            'res_model': 'download.excel.report',
            'view_type': 'form',
            'type': 'ir.actions.act_window',
            'context': self._context,
            'target': 'new',
        }


class JobEstimateTemplateLine(models.Model):
    _name = 'job.estimate.template.line'

    @api.depends('price_unit', 'product_uom_qty', 'uom_qty', 'discount')
    def _compute_amount(self):
        for rec in self:
            if rec.discount:
                disc_amount = (1 + rec.discount / 100)
                rec.price_subtotal = (rec.price_unit * rec.product_uom_qty * rec.uom_qty) * disc_amount
            else:
                rec.price_subtotal = rec.price_unit * rec.product_uom_qty * rec.uom_qty

    job_estimate_id = fields.Many2one('job.estimate.template', string="Job Estimate Id")
    labour_estimate_id = fields.Many2one('job.estimate.template', string="Labour Estimate")
    overhead_id = fields.Many2one('job.estimate.template', string="Over Head")
    subcon_id = fields.Many2one('job.estimate.template', string="Subcon Estimation")
    product_id = fields.Many2one(
        'product.product',
        string='Product',
        required=True
    )
    product_uom_qty = fields.Float(string='Quantity', digits=dp.get_precision('Product Price'), required=True,
                                   default=1.0)
    uom_qty = fields.Float(string='UoM Quantity', digits=dp.get_precision('Product Price'), required=True, default=1.0)
    product_uom = fields.Many2one('product.uom', related='product_id.product_tmpl_id.uom_id', string='Unit of Measure',
                                  required=True)
    price_unit = fields.Float('Unit Price', required=True, digits=dp.get_precision('Product Price'), default=0.0)
    price_subtotal = fields.Float(string='Subtotal', store=True, compute='_compute_amount')
    product_description = fields.Char(related='product_id.name', string='Description')
    discount = fields.Float(string='Adjustment (%)')
    company_id = fields.Many2one(related='job_estimate_id.company_id', string='Company', store=True, readonly=True)
    tax_id = fields.Many2many('account.tax', string='Taxes',
                              domain=['|', ('active', '=', False), ('active', '=', True)])

    job_type = fields.Selection(
        selection=[('material', 'Material'), ('labour', 'Labour'), ('overhead', 'Overhead'), ('subcon', 'Subcon')],
        string="Type")
    analytic_id = fields.Many2one(
        'account.analytic.account',
        'Analytic Account',
        store=True,
    )
    group_product_id = fields.Many2one("group.products", string="Group of Products")

    @api.onchange('group_product_id')
    def onchange_group_products(self):
        domain = {}
        if self.group_product_id:
            domain = {'product_id': [('id', 'in', self.group_product_id.product_ids.ids)]}
        elif not self.group_product_id:
            domain = {'product_id': [('id', '!=', False)]}
        # return {'domain': [('product_id', 'in', self.group_of_product_id.product_ids.ids)]}
        return {'domain': domain}