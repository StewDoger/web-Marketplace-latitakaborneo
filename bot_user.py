import re
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler
from handlers import (
    handle_message,
    handle_lihat_produk,
    handle_produk_detail,
    handle_cara_bayar,
    handle_cara_pembelian,
    handle_kembali_ke_menu
)

if __name__ == '__main__':
    application = ApplicationBuilder().token('7733149434:AAHY_v6O5Nv6hKQUyY74-BZx8nJUfN7ADFo').build()

    # Handler untuk pesan "halo" dan lain-lain
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Handler untuk tombol lihat produk
    application.add_handler(CallbackQueryHandler(handle_lihat_produk, pattern='^lihat_produk$'))

    # Handler untuk tombol produk yang akan menampilkan detail produk
    application.add_handler(CallbackQueryHandler(handle_produk_detail, pattern='^produk_'))

    # Handler untuk cara pembayaran
    application.add_handler(CallbackQueryHandler(handle_cara_bayar, pattern='^cara_bayar$'))

    # Handler untuk cara pembelian
    application.add_handler(CallbackQueryHandler(handle_cara_pembelian, pattern='^cara_pembelian$'))

    # Handler untuk kembali ke menu utama
    application.add_handler(CallbackQueryHandler(handle_kembali_ke_menu, pattern='^menu_utama$'))

    # Menjalankan bot
    application.run_polling()