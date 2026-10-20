from odoo import models, fields, api


class PosFoodCategory(models.Model):
    _name = 'pos.food.category'
    _description = 'Kategori Menu Makanan & Minuman'
    _order = 'name asc'

    name = fields.Char(string='Nama Kategori', required=True)
    description = fields.Text(string='Deskripsi')
    product_ids = fields.One2many(
        'pos.food.product',
        'category_id',
        string='Daftar Menu'
    )
    product_count = fields.Integer(
        string='Jumlah Menu',
        compute='_compute_product_count'
    )

    @api.depends('product_ids')
    def _compute_product_count(self):
        for record in self:
            record.product_count = len(record.product_ids)


class PosFoodProduct(models.Model):
    _name = 'pos.food.product'
    _description = 'Produk Menu Makanan & Minuman'
    _order = 'name asc'

    name = fields.Char(string='Nama Menu / Makanan', required=True)
    category_id = fields.Many2one(
        'pos.food.category',
        string='Kategori Menu',
        required=True
    )
    price = fields.Float(
        string='Harga Jual (Rp)',
        required=True,
        default=0.0
    )
    cost_price = fields.Float(
        string='Harga Modal / HPP (Rp)',
        default=0.0
    )
    is_available = fields.Boolean(
        string='Tersedia',
        default=True
    )
    description = fields.Text(string='Deskripsi / Komposisi')

