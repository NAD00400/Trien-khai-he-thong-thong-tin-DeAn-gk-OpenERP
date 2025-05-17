# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _  # Import để hiển thị thông báo lỗi

class NhaPhanPhoi(osv.osv):
    _name = 'nhaphanphoi.nhaphanphoi'

    _columns = {
        'name': fields.char('Tên nhà phân phối', required=True),
        'tax_code': fields.char('Mã số thuế', size=20, required=True),
        'address': fields.text('Địa chỉ', required=True),
        'phone': fields.char('Số điện thoại', required=True),
        'email': fields.char('Email', required=True),
        'contact_person': fields.char('Người liên hệ chính'),
        'device_ids': fields.one2many('device.device', 'distributor_id', string='Danh sách thiết bị'),
    }

    _sql_constraints = [
        ('tax_code_unique', 'unique(tax_code)', 'Mã số thuế không được trùng lặp!')
    ]

    def create(self, cr, uid, vals, context=None):
        if 'tax_code' in vals:
            existing_ids = self.search(cr, uid, [('tax_code', '=', vals['tax_code'])], context=context)
            if existing_ids:
                raise osv.except_osv(_('Lỗi ràng buộc!'), _('Mã số thuế không được trùng lặp.'))
        return super(NhaPhanPhoi, self).create(cr, uid, vals, context)

    def write(self, cr, uid, ids, vals, context=None):
        if 'tax_code' in vals:
            existing_ids = self.search(cr, uid, [('tax_code', '=', vals['tax_code'])], context=context)
            if existing_ids:
                raise osv.except_osv(_('Lỗi ràng buộc!'), _('Mã số thuế không được trùng lặp.'))
        return super(NhaPhanPhoi, self).write(cr, uid, ids, vals, context)

NhaPhanPhoi()