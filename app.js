require('dotenv').config(); // Load environment variables from .env file
const express = require('express');
const path = require('path');
const mongoose = require('mongoose');
const app = express();

// Koneksi ke MongoDB menggunakan URI dari file .env
mongoose.connect('mongodb://localhost:27017/chatbot', { 
    useNewUrlParser: true, 
    useUnifiedTopology: true 
})
    .then(() => {
        console.log('Successfully connected to MongoDB');
    })
    .catch((err) => {
        console.error('Error connecting to MongoDB:', err);
    });

// Definisikan model Item
const Item = mongoose.model('products', new mongoose.Schema({
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
app.get('/inventory', async (req, res) => {
    try {
        // Ambil data produk dari MongoDB (atau sumber data lainnya)
        const products = await Item.find(); // atau query yang sesuai dengan struktur aplikasi Anda
        res.render('inventory', { products }); // Kirim data products ke view
    } catch (error) {
        console.error(error);
        res.status(500).send("Server Error");
    }
});

// Route untuk halaman home
app.get('/', (req, res) => {
    res.render('index'); // Renders views/index.ejs
});

// Route untuk halaman konsultasi
app.get('/konsultasi', (req, res) => {
    res.render('konsultasi');
});

// Route untuk halaman produk
app.get('/produk', (req, res) => {
    res.render('produk');
});

// Route untuk halaman hampers
app.get('/hampers', (req, res) => {
    res.render('hampers'); // Renders views/hampers.ejs
});

// Route untuk halaman order
app.get('/order', (req, res) => {
    res.render('order'); // Renders views/order.ejs
});

// Route untuk menerima POST request dan menambah produk
app.post('/submit_produk', async (req, res) => {
    try {
        const { 'nama-produk': name, 'deskripsi-produk': description, 'harga-produk': price, 'stok-produk': stock } = req.body;

        const newProduct = new Item({
            name,
            description,
            price,
            stock
        });

        await newProduct.save(); // Simpan produk baru
        res.redirect('/inventory'); // Redirect ke halaman inventory setelah produk disimpan
    } catch (err) {
        console.error('Terjadi kesalahan saat menambahkan produk', err);
        res.status(500).send('Terjadi kesalahan saat menambahkan produk');
    }
});

// Mulai server
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
