// routes/adminRoutes.js
const express = require('express');
const router = express.Router();
const Produk = require('../models/stock');

// Rute untuk menampilkan halaman update stok
router.get('/update-stok', async (req, res) => {
    try {
        const products = await Produk.find();  // Ambil data produk dari database
        res.render('admin/update-stok', { products });
    } catch (err) {
        console.error(err);
        res.status(500).send('Terjadi kesalahan saat mengambil data produk');
    }
});

// Rute untuk menangani pembaruan stok
router.post('/update-stok', async (req, res) => {
    try {
        const productIds = Object.keys(req.body);  // Ambil semua kunci (ID produk)
        for (let id of productIds) {
            if (id.startsWith('stock_')) {
                const productId = id.split('_')[1];  // Ambil ID produk dari kunci
                const stockValue = req.body[id];  // Ambil nilai stok yang baru

                // Update stok produk di database
                await Produk.findByIdAndUpdate(productId, { stock: stockValue });
            }
        }

        // Setelah pembaruan selesai, arahkan ke halaman admin dengan pesan sukses
        res.redirect('/admin/update-stok');
    } catch (err) {
        console.error(err);
        res.status(500).send('Terjadi kesalahan saat memperbarui stok produk');
    }
});

module.exports = router;
