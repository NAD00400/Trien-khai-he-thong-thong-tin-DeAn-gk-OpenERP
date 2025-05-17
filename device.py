# -*- coding: utf-8 -*-
from openerp.osv import fields, osv
from openerp.tools.translate import _  # Import để hiển thị thông báo lỗi

class device(osv.osv):
    _name = 'device.device'

    def _get_status(self, cr, uid, ids, field_name, args, context=None):
        res = {}
        for record in self.browse(cr, uid, ids, context=context):
            res[record.id] = "Đang hoạt động" if record.active else "Đã ngưng hoạt động"
        return res

    _columns = {
        'device_code': fields.char('Mã thiết bị', size=10, required=True),
        'name': fields.char('Tên thiết bị', size=100, required=True),
        'date_joined': fields.date('Ngày nhập'),
        'storage_id': fields.many2one('storage.storage', string='Kho thiết bị', required=True),
        'active': fields.boolean('Hoạt động'),
        'position': fields.char('Vị trí', required=True),
        'status': fields.function(_get_status, type='char', string='Trạng thái', store=True),
        'sl': fields.integer('Số lượng'),
        'dg': fields.float('Đơn giá'),
        'distributor_id': fields.many2one('nhaphanphoi.nhaphanphoi', string='Nhà phân phối', required=True),
    }

    _defaults = {
        'active': True
    }

    _sql_constraints = [
        ('device_code_unique', 'unique(device_code)', 'Mã thiết bị không được trùng lặp!')
    ]

    # Thêm ràng buộc kiểm tra số lượng, đơn giá và mã thiết bị
    def check_constraints(self, cr, uid, vals, context=None):
        if 'sl' in vals and vals['sl'] <= 0:
            raise osv.except_osv(_('Lỗi ràng buộc!'), _('Số lượng phải lớn hơn 0.'))
        if 'dg' in vals and vals['dg'] <= 0:
            raise osv.except_osv(_('Lỗi ràng buộc!'), _('Đơn giá phải lớn hơn 0.'))
        if 'device_code' in vals:
            existing_ids = self.search(cr, uid, [('device_code', '=', vals['device_code'])], context=context)
            if existing_ids:
                raise osv.except_osv(_('Lỗi ràng buộc!'), _('Mã thiết bị không được trùng lặp.'))
        return True

    def create(self, cr, uid, vals, context=None):
        self.check_constraints(cr, uid, vals, context)
        return super(device, self).create(cr, uid, vals, context)

    def write(self, cr, uid, ids, vals, context=None):
        self.check_constraints(cr, uid, vals, context)
        return super(device, self).write(cr, uid, ids, vals, context)

device()
