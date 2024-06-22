const express = require('express');
const path = require('path');
const app = express();

// Set the views directory and view engine
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

// Middleware untuk menyajikan file statis dari direktori 'public'
app.use(express.static(path.join(__dirname, 'public')));

// Middleware untuk memungkinkan akses __dirname dari semua template
app.use((req, res, next) => {
    res.locals.__dirname = __dirname;
    next();
});

// Define routes

// Route for the home page
app.get('/', (req, res) => {
    res.render('index'); // Renders views/index.ejs
});

// Route for konsultasi page
app.get('/konsultasi', (req, res) => {
    res.render('konsultasi'); // Renders views/konsultasi.ejs
});

// Route for produk page
app.get('/produk', (req, res) => {
    res.render('produk'); // Renders views/produk.ejs
});

// Route for hampers page
app.get('/hampers', (req, res) => {
    res.render('hampers'); // Renders views/hampers.ejs
});

// Route for order page
app.get('/order', (req, res) => {
    res.render('order'); // Renders views/order.ejs
});


// Start the server
const PORT = process.env.PORT || 1000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
