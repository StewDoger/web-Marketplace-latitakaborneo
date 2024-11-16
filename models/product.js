const mongoose = require('mongoose');

const produkSchema = new mongoose.Schema({
    name: String,
    description: String,
    price: Number,
    stock: Number
});

const Produk = mongoose.model('Produk', produkSchema);

module.exports = Produk;
