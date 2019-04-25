from odoo import models, fields, api, _
from odoo import exceptions, _
import xlwt
import base64
from StringIO import StringIO
import xlrd
import tempfile
import binascii


class download_excel_report(models.TransientModel):
    _name = 'download.excel.report'

    excel_file = fields.Binary('Job Estimate Template')
    file_name = fields.Char('Excel File', size=64)


class ImportJobEstimateWizard(models.TransientModel):
    _name = 'import.job.estimate.wizard'

    import_file = fields.Binary(string="Import File")

    # Import Template from wizard
    @api.multi
    def import_template(self):
        fp = tempfile.NamedTemporaryFile(suffix=".xls")
        if self.import_file:
            fp.write(binascii.a2b_base64(self.import_file))
            fp.seek(0)
            workbook = xlrd.open_workbook(fp.name)

            if workbook.sheet_by_index(0):
                sheet1 = workbook.sheet_by_index(0)
                sheet1_name = sheet1.name
                sheet1_data = {}
                for row_n in range(sheet1.nrows):
                    if row_n != 0:
                        line = list(
                            map(lambda row: isinstance(row.value, str) and row.value.encode('utf-8') or str(row.value),
                                sheet1.row(row_n)))
                        sheet1_data['var_internal_ref'] = line[0]
                        sheet1_data['name'] = line[1]
                        sheet1_data['uom'] = line[2]
                        for sheets in workbook.sheets():
                            if sheets.name == 'Material Estimation':
                                job_estimate_ids = []
                                for row_no in range(sheets.nrows):
                                    if row_no != 0:
                                        line = list(map(
                                            lambda row: isinstance(row.value, str) and row.value.encode('utf-8') or str(
                                                row.value), sheets.row(row_no)))
                                        product_ids_material = self.env['product.product'].search(
                                            [('default_code', '=', line[1])])
                                        job_estimate_ids.append((0, 0, {
                                            'product_id': product_ids_material.id,
                                            'product_description': line[3],
                                            'product_uom_qty': line[4],
                                            'price_unit': line[6],
                                            'discount': line[7],
                                            'job_type': 'material',
                                        }))
                                sheet1_data.update({
                                    'job_estimate_ids': job_estimate_ids,
                                })

                            if sheets.name == 'Labour Estimation':
                                labour_estimate_ids = []
                                for row_no in range(sheets.nrows):
                                    if row_no != 0:
                                        line = list(map(
                                            lambda row: isinstance(row.value, str) and row.value.encode('utf-8') or str(
                                                row.value), sheets.row(row_no)))
                                        product_ids_labour = self.env['product.product'].search(
                                            [('default_code', '=', line[1])])
                                        labour_estimate_ids.append((0, 0, {
                                            'product_id': product_ids_labour.id,
                                            'product_description': line[3],
                                            'product_uom_qty': line[4],
                                            'uom_qty': line[5],
                                            'price_unit': line[7],
                                            'discount': line[8],
                                            'job_type': 'labour',
                                        }))
                                sheet1_data.update({
                                    'labour_estimate_ids': labour_estimate_ids,
                                })

                            if sheets.name == 'Subcon Estimation':
                                subcon_estimation_ids = []
                                for row_no in range(sheets.nrows):
                                    if row_no != 0:
                                        line = list(map(
                                            lambda row: isinstance(row.value, str) and row.value.encode('utf-8') or str(
                                                row.value), sheets.row(row_no)))
                                        product_ids_subcon = self.env['product.product'].search(
                                            [('default_code', '=', line[1])])
                                        subcon_estimation_ids.append((0, 0, {
                                            'product_id': product_ids_subcon.id,
                                            'product_description': line[3],
                                            'product_uom_qty': line[4],
                                            'price_unit': line[6],
                                            'discount': line[7],
                                            'job_type': 'subcon',
                                        }))
                                sheet1_data.update({
                                    'subcon_estimation_ids': subcon_estimation_ids,
                                })

                            if sheets.name == 'Overhead Estimation':
                                overhead_ids = []
                                for row_no in range(sheets.nrows):
                                    if row_no != 0:
                                        line = list(map(
                                            lambda row: isinstance(row.value, str) and row.value.encode('utf-8') or str(
                                                row.value), sheets.row(row_no)))
                                        product_ids_overhead = self.env['product.product'].search(
                                            [('default_code', '=', line[1])])
                                        overhead_ids.append((0, 0, {
                                            'product_id': product_ids_overhead.id,
                                            'product_description': line[3],
                                            'product_uom_qty': line[4],
                                            'price_unit': line[6],
                                            'discount': line[7],
                                            'job_type': 'overhead',
                                        }))
                                sheet1_data.update({
                                    'overhead_ids': overhead_ids,
                                })
                        aa = self.env['job.estimate.template'].create(sheet1_data)
        else:
            raise exceptions.UserError("File not selected!")
        return aa

    # Export Blank Template from wizard
    @api.multi
    def export_template(self):
        file_name = 'JobEstimateTemplate.xls'
        # print("XXXXXXXXX", self)
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
