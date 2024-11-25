require('dotenv').config(); // Load environment variables from .env file
const express = require('express');
const path = require('path');
const mongoose = require('mongoose');
const session = require('express-session');
const app = express();

// Middleware session
app.use(
    session({
        secret: 'in81705yv98y0r008900000f0y034r', // Ganti dengan kunci rahasia Anda
        resave: false,
        saveUninitialized: true,
        cookie: { secure: false } // Set `true` jika menggunakan HTTPS
    })
);

// Middleware untuk memeriksa login
function isAuthenticated(req, res, next) {
    if (req.session && req.session.isLoggedIn) {
        return next(); // Jika sudah login, lanjutkan
    }
    res.redirect('/login'); // Jika belum login, alihkan ke halaman login
}

// Koneksi ke MongoDB
mongoose.connect('mongodb://devi:deviayu123@ac-1abopc9-shard-00-00.etzoacx.mongodb.net:27017,ac-1abopc9-shard-00-01.etzoacx.mongodb.net:27017,ac-1abopc9-shard-00-02.etzoacx.mongodb.net:27017/chatbot?ssl=true&replicaSet=atlas-btvwbf-shard-0&authSource=admin&retryWrites=true&w=majority&appName=Data', {
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

// Middleware untuk parsing body request
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// Tentukan PORT
const PORT = process.env.PORT || 3000;

// Route untuk halaman home
app.get('/', (req, res) => {
    res.render('index');
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
    res.render('hampers');
});

// Route untuk halaman order
app.get('/order', (req, res) => {
    res.render('order');
});

// Route untuk halaman login
app.get('/login', (req, res) => {
    res.render('login', { error: null });
});

// Proses login
app.post('/login', (req, res) => {
    const { username, password } = req.body;

    if (username === 'admin' && password === 'borneo') {
        req.session.isLoggedIn = true;
        res.redirect('/inventory');
    } else {
        res.render('login', { error: 'Username atau password salah' });
    }
});

// Logout
app.get('/logout', (req, res) => {
    req.session.destroy(() => {
        res.redirect('/login');
    });
});

// Route untuk halaman inventory (dengan autentikasi)
app.get('/inventory', isAuthenticated, async (req, res) => {
    try {
        const products = await Item.find(); // Ambil data produk dari database
        res.render('inventory', { products });
    } catch (error) {
        console.error(error);
        res.status(500).send("Server Error");
    }
});

// Route untuk menambah produk
app.post('/submit_produk', isAuthenticated, async (req, res) => {
    try {
        const { 'nama-produk': name, 'deskripsi-produk': description, 'harga-produk': price, 'stok-produk': stock } = req.body;

        const newProduct = new Item({
            name,
            description,
            price,
            stock
        });

        await newProduct.save();
        res.redirect('/inventory');
    } catch (err) {
        console.error('Terjadi kesalahan saat menambahkan produk', err);
        res.status(500).send('Terjadi kesalahan saat menambahkan produk');
    }
});

// Route untuk update stok produk
app.post('/inventory/update/:id', isAuthenticated, async (req, res) => {
    try {
        const { id } = req.params;
        const { stock } = req.body;

        if (!stock || isNaN(stock) || stock < 0) {
            return res.status(400).send('Stok tidak valid');
        }

        const updatedProduct = await Item.findByIdAndUpdate(
            id,
            { stock: Number(stock) },
            { new: true }
        );

        if (!updatedProduct) {
            return res.status(404).send('Produk tidak ditemukan');
        }

        res.redirect('/inventory');
    } catch (err) {
        console.error('Terjadi kesalahan saat mengupdate stok:', err);
        res.status(500).send('Terjadi kesalahan saat mengupdate stok');
    }
});

// Route untuk menghapus produk
app.post('/inventory/delete/:id', isAuthenticated, async (req, res) => {
    try {
        const { id } = req.params;

        const deletedProduct = await Item.findByIdAndDelete(id);

        if (!deletedProduct) {
            return res.status(404).send('Produk tidak ditemukan');
        }

        res.redirect('/inventory');
    } catch (err) {
        console.error('Terjadi kesalahan saat menghapus produk:', err);
        res.status(500).send('Terjadi kesalahan saat menghapus produk');
    }
});

// Mulai server
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});