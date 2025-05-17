# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _  # Import để hiển thị thông báo lỗi

class storage(osv.osv):
    _name = 'storage.storage'

    def _get_status(self, cr, uid, ids, field_name, args, context=None):
        res = {}
        for record in self.browse(cr, uid, ids, context=context):
            res[record.id] = "Đang hoạt động" if record.active else "Ngưng hoạt động"
        return res

    _columns = {
        'code': fields.char('Mã kho', size=10, required=True),
        'name': fields.char('Tên kho', size=100, required=True),
        'active': fields.boolean('Hoạt động'),
        'create_date': fields.datetime('Ngày tạo'),
        'position': fields.char('Vị trí kho'),
        'manager': fields.char('Người quản lý'),
        'device_ids': fields.one2many('device.device', 'storage_id', string='Thiết bị'),
        'status': fields.function(_get_status, type='char', string='Trạng thái', store=True),
    }

    _defaults = {
        'active': True
    }

    _sql_constraints = [
        ('storage_code_unique', 'unique(code)', 'Mã kho không được trùng lặp!')
    ]

    # Thêm ràng buộc kiểm tra mã kho không trùng lặp
    def check_constraints(self, cr, uid, vals, context=None):
        if 'code' in vals:
            existing_ids = self.search(cr, uid, [('code', '=', vals['code'])], context=context)
            if existing_ids:
                raise osv.except_osv(_('Lỗi ràng buộc!'), _('Mã kho không được trùng lặp.'))
        return True

    def create(self, cr, uid, vals, context=None):
        self.check_constraints(cr, uid, vals, context)
        return super(storage, self).create(cr, uid, vals, context)

    def write(self, cr, uid, ids, vals, context=None):
        self.check_constraints(cr, uid, vals, context)
        return super(storage, self).write(cr, uid, ids, vals, context)

storage()
