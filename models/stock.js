// models/produk.js
const mongoose = require('mongoose');

const stockSchema = new mongoose.Schema({
    name: String,
    description: String,
    price: Number,
    stock: Number
});

const Stock = mongoose.model('Stock', stockSchema);

module.exports = Stock;
