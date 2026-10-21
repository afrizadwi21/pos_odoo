{
    "name": "POS Odoo",
    "version": "1.0.0",
    "summary": "Modul Penjualan dan Point of Sale (POS)",
    "category": "Sales/Point of Sale",
    "author": "Custom",
    "depends": ["base"],
    "data": [
        "security/ir.access.csv",
        "views/pos_order_views.xml",
        "views/pos_product_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "pos_odoo/static/src/scss/pos_mobile.scss",
        ],
    },
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}
