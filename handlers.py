from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from bson import ObjectId
from database import products_collection
from constants import cara_bayar, cara_pembelian

# Fungsi untuk menampilkan opsi awal kepada pengguna
async def show_options(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Lihat Produk", callback_data='lihat_produk')],
        [InlineKeyboardButton("Cara Pembayaran", callback_data='cara_bayar')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
        await update.callback_query.message.reply_text('Silakan pilih opsi di bawah ini:', reply_markup=reply_markup)
    elif update.message:
        await update.message.reply_text('Silakan pilih opsi di bawah ini:', reply_markup=reply_markup)

# Fungsi untuk kembali ke menu utama
async def handle_kembali_ke_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("Lihat Produk", callback_data='lihat_produk')],
        [InlineKeyboardButton("Cara Pembayaran", callback_data='cara_bayar')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text('Silakan pilih opsi di bawah ini:', reply_markup=reply_markup)

# Fungsi untuk menampilkan daftar produk dari MongoDB
async def handle_lihat_produk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    produk_keyboard = []
    try:
        # Mengambil semua produk dari koleksi
        for produk in products_collection.find():
            # Pastikan produk memiliki kunci yang diperlukan
            if 'name' in produk and 'description' in produk:
                produk_keyboard.append([InlineKeyboardButton(produk['name'], callback_data=f"produk_{produk['_id']}")])

        # Menambahkan opsi kembali ke menu utama
        produk_keyboard.append([InlineKeyboardButton("Kembali ke Menu Utama", callback_data='menu_utama')])
        reply_markup = InlineKeyboardMarkup(produk_keyboard)

        if produk_keyboard:
            await query.edit_message_text(text="Pilih produk untuk melihat detailnya:", reply_markup=reply_markup)
        else:
            await query.edit_message_text(text="Tidak ada produk yang tersedia.")
    except Exception as e:
        await query.edit_message_text(text="Terjadi kesalahan saat mengambil daftar produk.")
        print(f"Error: {e}")

# Fungsi untuk menampilkan detail produk yang dipilih
async def handle_produk_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    produk_id = query.data.split('_')[1]

    try:
        produk = products_collection.find_one({"_id": ObjectId(produk_id)})
        if produk:
            # Memastikan bahwa deskripsi adalah list dan mengonversinya menjadi string
            detail_produk = f"{produk['name']}\n\nDeskripsi: {(produk['description'])}\nHarga: Rp {produk['price']:,}\nStok: {produk['stock']} buah"
            keyboard = [
                [InlineKeyboardButton("Cara Pembelian", callback_data='cara_pembelian')],
                [InlineKeyboardButton("Kembali ke Menu Utama", callback_data='menu_utama')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text=detail_produk, reply_markup=reply_markup)
        else:
            await query.edit_message_text(text="Detail produk tidak ditemukan.")
    except Exception as e:
        await query.edit_message_text(text="Terjadi kesalahan saat mengambil detail produk.")
        print(f"Error: {e}")

# Fungsi untuk menampilkan cara pembayaran
async def handle_cara_bayar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [[InlineKeyboardButton("Kembali ke Menu Utama", callback_data='menu_utama')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=cara_bayar, reply_markup=reply_markup)

# Fungsi untuk menampilkan cara pembelian
async def handle_cara_pembelian(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [[InlineKeyboardButton("Kembali ke Menu Utama", callback_data='menu_utama')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=cara_pembelian, reply_markup=reply_markup)

# Fungsi untuk menangani pesan yang diterima
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.lower()

    if any(greet in user_message for greet in ['halo', 'hi', 'selamat pagi', 'selamat siang', 'selamat malam', 'hey', 'hai']):
        await show_options(update, context)
    elif any(term in user_message for term in ['produk', 'daftar produk', 'lihat produk', 'tampilkan produk']):
        await handle_lihat_produk(update, context)
    elif any(term in user_message for term in ['cara beli', 'pembelian']):
        await handle_cara_pembelian(update, context)
    elif any(term in user_message for term in ['cara bayar', 'metode pembayaran']):
        await handle_cara_bayar(update, context)
    elif any(term in user_message for term in ['terima kasih', 'makasih']):
        await update.message.reply_text("Sama-sama! Jika ada pertanyaan lain, silakan tanyakan.", 
                                         reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Kembali ke Menu Utama", callback_data='menu_utama')]]))
    else:
        await update.message.reply_text("Maaf, kami tidak menemukan jawaban untuk pertanyaan Anda. Silakan coba dengan kata kunci lain.", 
                                         reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Kembali ke Menu Utama", callback_data='menu_utama')]]))

# Memastikan callback_query diproses dengan benar
async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'menu_utama':
        await handle_kembali_ke_menu(update, context)
    elif query.data.startswith('produk_'):
        await handle_produk_detail(update, context)
    elif query.data == 'cara_bayar':
        await handle_cara_bayar(update, context)
    elif query.data == 'cara_pembelian':
        await handle_cara_pembelian(update, context)