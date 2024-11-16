require('dotenv').config();
const express = require('express');
const path = require('path');
const mongoose = require('mongoose');
const app = express();

// Koneksi ke MongoDB
mongoose.connect(process.env.MONGO_URI, { useNewUrlParser: true, useUnifiedTopology: true })
    .then(() => console.log('Connected to MongoDB'))
    .catch((err) => console.error('Failed to connect to MongoDB', err));

// Definisikan Model Item
const Item = mongoose.model('Item', new mongoose.Schema({
    name: String,
    description: String,
    price: Number,
    stock: Number
}));

// Middleware
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');
app.use(express.static(path.join(__dirname, 'public')));

const PORT = process.env.PORT || 3000;

// Route untuk halaman inventory
app.get('/inventory', (req, res) => {
    Item.find()  // Ambil semua data produk dari database
        .then((items) => {
            res.render('inventory', { items }); // Kirim data produk ke tampilan 'inventory.ejs'
        })
        .catch((err) => {
            console.error('Error fetching items:', err);
            res.status(500).send('Error retrieving data');
        });
});

// Route lainnya
app.get('/', (req, res) => {
    res.render('index'); // Renders views/index.ejs
});

app.get('/konsultasi', (req, res) => {
    res.render('konsultasi'); // Renders views/konsultasi.ejs
});

app.get('/hampers', (req, res) => {
    res.render('hampers'); // Renders views/hampers.ejs
});

app.get('/order', (req, res) => {
    res.render('order'); // Renders views/order.ejs
});

// Mulai server
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});