require('dotenv').config(); // Load environment variables from .env file
const express = require('express');
const path = require('path');
const mongoose = require('mongoose');
const app = express();

// Koneksi ke MongoDB menggunakan URI dari file .env
mongoose.connect(process.env.MONGO_URI, { useNewUrlParser: true, useUnifiedTopology: true })
    .then(() => {
        console.log('Successfully connected to MongoDB');
    })
    .catch((err) => {
        console.error('Error connecting to MongoDB:', err);
    });

// Definisikan model Item
const Item = mongoose.model('Item', new mongoose.Schema({
    name: String,
    description: String,
    price: Number,
    stock: Number
}));

// Middleware untuk set up views dan static files
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');
app.use(express.static(path.join(__dirname, 'public')));

// Middleware untuk menangani parsing body request (POST, PUT)
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// Menentukan PORT
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

// Route untuk halaman home
app.get('/', (req, res) => {
    res.render('index' , { dirname: __dirname }); // Renders views/index.ejs
});

// Route untuk halaman konsultasi
app.get('/konsultasi', (req, res) => {
    res.render('konsultasi', { dirname: __dirname });
});

// Route untuk halaman rpduk
app.get('/produk', (req, res) => {
    res.render('produk', { dirname: __dirname });
});

// Route untuk halaman hampers
app.get('/hampers', (req, res) => {
    res.render('hampers' , { dirname: __dirname }); // Renders views/hampers.ejs
});

// Route untuk halaman order
app.get('/order', (req, res) => {
    res.render('order' , { dirname: __dirname }); // Renders views/order.ejs
});

// Mulai server
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
