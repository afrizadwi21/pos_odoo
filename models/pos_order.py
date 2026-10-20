from odoo import models, fields, api


class PosCustomOrder(models.Model):
    _name = 'pos.custom.order'
    _description = 'Order Penjualan Kasir'
    _order = 'order_date desc, id desc'

    name = fields.Char(
        string='No. Transaksi',
        required=True,
        copy=False,
        readonly=True,
        default='Baru'
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Pelanggan'
    )
    order_date = fields.Datetime(
        string='Tanggal Transaksi',
        default=fields.Datetime.now,
        required=True
    )
    cashier_id = fields.Many2one(
        'res.users',
        string='Kasir',
        default=lambda self: self.env.user,
        required=True
    )
    payment_method = fields.Selection([
        ('cash', 'Tunai (Cash)'),
        ('qris', 'QRIS'),
        ('transfer', 'Transfer Bank'),
        ('debit', 'Kartu Debit/Kredit'),
    ], string='Metode Pembayaran', default='cash', required=True)

    line_ids = fields.One2many(
        'pos.custom.order.line',
        'order_id',
        string='Daftar Barang'
    )
    total_amount = fields.Float(
        string='Total Belanja',
        compute='_compute_total_amount',
        store=True
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('paid', 'Lunas / Selesai'),
        ('cancel', 'Dibatalkan'),
    ], string='Status', default='draft', required=True)

    note = fields.Text(string='Catatan Transaksi')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Baru') == 'Baru':
                current_year = fields.Date.today().year
                count = self.search_count([]) + 1
                vals['name'] = f"POS/{current_year}/{count:04d}"
        return super().create(vals_list)

    @api.depends('line_ids.subtotal')
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = sum(line.subtotal for line in record.line_ids)

    def action_pay(self):
        self.write({'state': 'paid'})

    def action_cancel(self):
        self.write({'state': 'cancel'})

    def action_draft(self):
        self.write({'state': 'draft'})


class PosCustomOrderLine(models.Model):
    _name = 'pos.custom.order.line'
    _description = 'Detail Item Transaksi Kasir'

    order_id = fields.Many2one(
        'pos.custom.order',
        string='Order Ref',
        ondelete='cascade',
        required=True
    )
    product_id = fields.Many2one(
        'pos.food.product',
        string='Pilih Menu',
        domain="[('is_available', '=', True)]"
    )
    product_name = fields.Char(
        string='Nama Menu / Item',
        required=True
    )
    qty = fields.Float(
        string='Jumlah (Qty)',
        default=1.0,
        required=True
    )
    price_unit = fields.Float(
        string='Harga Satuan (Rp)',
        default=0.0,
        required=True
    )
    subtotal = fields.Float(
        string='Subtotal (Rp)',
        compute='_compute_subtotal',
        store=True
    )

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.product_name = self.product_id.name
            self.price_unit = self.product_id.price

    @api.depends('qty', 'price_unit')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.qty * line.price_unit
