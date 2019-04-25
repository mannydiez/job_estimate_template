# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError, ValidationError


class SaleEstimatelineJob(models.Model):
    _inherit = "sale.estimate.line.job"

    job_estimate_template_id = fields.Many2one('job.estimate.template', string="Variable Reference")
    var_qty = fields.Float(string="Variable Quantity", digits=dp.get_precision('Product Unit of Measure'))

    # Subtotal of each line of each tab
    @api.depends('price_unit', 'product_uom_qty', 'discount', 'uom_qty_est')
    def _compute_amount(self):
        for rec in self:
            if rec.uom_qty_est:
                if rec.discount:
                    disc_amount = (rec.discount + 100) / 100
                    rec.price_subtotal = (rec.price_unit * rec.product_uom_qty * rec.uom_qty_est) * (disc_amount)
                else:
                    rec.price_subtotal = rec.price_unit * rec.product_uom_qty * rec.uom_qty_est
            else:
                if rec.discount:
                    disc_amount = (rec.discount + 100) / 100
                    rec.price_subtotal = (rec.price_unit * rec.product_uom_qty) * (disc_amount)
                else:
                    rec.price_subtotal = rec.price_unit * rec.product_uom_qty


class SaleEstimateJob(models.Model):
    _inherit = 'sale.estimate.job'

    variable_ids = fields.One2many('sale.estimate.variable.line', 'variable_id', string="Variable")

    @api.onchange('variable_ids')
    def auto_fill_line_obj(self):
        material_list = []
        labour_list = []
        subcon_list = []
        overhead_list = []
        if self.variable_ids:
            for obj in self.variable_ids:
                for line in obj.job_variable_id.job_estimate_ids:
                    material_list.append((0, 0, {
                        'group_product_id': line.group_product_id.id if line.group_product_id else False,
                        'product_id': line.product_id.id,
                        'product_uom_qty': line.product_uom_qty * obj.qty,
                        'product_uom': line.product_uom.id,
                        'price_unit': line.price_unit,
                        'price_subtotal': line.price_subtotal * obj.qty,
                        'product_description': line.product_description,
                        'discount': line.discount,
                        'job_type': line.job_type,
                        'job_estimate_template_id': obj.job_variable_id.id,
                        'var_qty': obj.qty,
                    }))
                self.estimate_ids = material_list
                for line in obj.job_variable_id.labour_estimate_ids:
                    labour_list.append((0, 0, {
                        'group_product_id': line.group_product_id.id if line.group_product_id else False,
                        'product_id': line.product_id.id,
                        'product_uom_qty': line.product_uom_qty * obj.qty,
                        'product_uom': line.product_uom.id,
                        'price_unit': line.price_unit,
                        'price_subtotal': line.price_subtotal * obj.qty,
                        'product_description': line.product_description,
                        'discount': line.discount,
                        'job_type': line.job_type,
                        'job_estimate_template_id': obj.job_variable_id.id,
                        'var_qty': obj.qty,
                        'uom_qty': 1.00,
                    }))
                self.labour_estimate_line_ids = labour_list
                for line in obj.job_variable_id.overhead_ids:
                    overhead_list.append((0, 0, {
                        'group_product_id': line.group_product_id.id if line.group_product_id else False,
                        'product_id': line.product_id.id,
                        'product_uom_qty': line.product_uom_qty * obj.qty,
                        'product_uom': line.product_uom.id,
                        'price_unit': line.price_unit,
                        'price_subtotal': line.price_subtotal * obj.qty,
                        'product_description': line.product_description,
                        'discount': line.discount,
                        'job_type': line.job_type,
                        'job_estimate_template_id': obj.job_variable_id.id,
                        'var_qty': obj.qty,
                    }))
                self.overhead_estimate_line_ids = overhead_list
                for line in obj.job_variable_id.subcon_estimation_ids:
                    subcon_list.append((0, 0, {
                        'group_product_id': line.group_product_id.id if line.group_product_id else False,
                        'product_id': line.product_id.id,
                        'product_description': line.product_description,
                        'product_uom_qty': line.product_uom_qty,
                        'product_uom': line.product_uom.id,
                        'price_unit': line.price_unit,
                        'discount': line.discount,
                        'price_subtotal': line.price_subtotal,
                        'job_type': 'subcon',
                        'job_estimate_template_id': obj.job_variable_id.id,
                        'var_qty': obj.qty,

                    }))
                self.subcon_estimation_line_ids = subcon_list

    # if not self.variable_ids:
    # 	obj = self.env['job.estimate.template'].search([('id','=',self.variable_ids.job_variable_id.id)]).mapped('job_estimate_ids')
    # 	print("!!!!!!!!!!!!",obj)


# 	@api.constrains('variable_ids')
# 	def check_variable_ids(self):
# 		SaleEstimateVariableLine = self.variable_ids.search([('variable_id','=',self.id)])
# 		list = [line.job_variable_id.id for line in SaleEstimateVariableLine]
# 		print "====================================",list,SaleEstimateVariableLine
# 		if len(list) > 1:
# 			raise ValidationError("You have already mentioned this Variable in another line")

class SaleEstimateVariableLine(models.Model):
    _name = 'sale.estimate.variable.line'

    # Add subtotal of each line of each tab in Variable tab Subtotal.
    # @api.depends('qty', 'variable_id.estimate_ids', 'variable_id.labour_estimate_line_ids',
    #              'variable_id.overhead_estimate_line_ids', 'variable_id.subcon_estimation_line_ids')
    # def _compute_amount(self):
    #     for rec in self:
    #         # saleestlineobj = self.env['sale.estimate.line.job'].search(
    #         #     [('job_estimate_template_id', '=', rec.job_variable_id.id), ('var_qty', '=', rec.qty),
    #         #      ('estimate_id', '=', rec.variable_id.id)])
    #         # print("XXXXXXXXXXXXXXXXXXXXXXXXX", saleestlineobj)
    #         saleestlineobj = self.env['sale.estimate.line.job'].search(
    #             [('job_estimate_template_id', '=', rec.job_variable_id.id), ('estimate_id', '=', rec.variable_id.id)])
    #         subtotal = float(sum(data.price_subtotal for data in saleestlineobj))
    #         # print("CCCCCCCCCCCCCCCCCCCCCCCC", subtotal)
    #         rec.subtotal = subtotal

    @api.depends('qty', 'job_variable_id')
    def _compute_amount_var(self):
        for rec in self:
            grand_total = 0.0
            for total in rec.job_variable_id.job_estimate_ids:
                grand_total += total.price_subtotal
            for total1 in rec.job_variable_id.labour_estimate_ids:
                grand_total += total1.price_subtotal
            for total2 in rec.job_variable_id.subcon_estimation_ids:
                grand_total += total2.price_subtotal
            for total3 in rec.job_variable_id.overhead_ids:
                grand_total += total3.price_subtotal
            # print("Grand4Grand4Grand4", grand_total)
            rec.subtotal = (rec.qty * grand_total)
            # print("ASASASASASASASASS", rec.subtotal)


    variable_id = fields.Many2one('sale.estimate.job', string="Variable Id")
    job_variable_id = fields.Many2one('job.estimate.template', string="Variable")
    qty = fields.Float(string="Quantity", digits=(16, 2), default=1.0)
    uom = fields.Char(
        # related='job_variable_id.uo_measure',
        string="UoM")
    subtotal = fields.Float(compute='_compute_amount_var', string='Subtotal')

# 	_sql_constraints = [
#         ('uniq_job_variable_id', 'unique(variable_id,job_variable_id)', 'You have already mentioned this Variable in another line'),
#         ]
