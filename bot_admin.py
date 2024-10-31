from telegram import Update
from telegram.ext import ContextTypes

# ID chat admin, pastikan untuk mengisi dengan ID chat yang benar
ADMIN_CHAT_ID = '5287460125'

# Fungsi untuk menghubungi admin
async def handle_chat_with_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Anda terhubung dengan admin. Silakan tulis pesan Anda:")
    context.user_data['chat_with_admin'] = True  # Tandai bahwa pengguna sedang chat dengan admin

# Fungsi untuk menangani pesan dari pengguna
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Jika pengguna sedang dalam chat dengan admin
    if context.user_data.get('chat_with_admin'):
        admin_message = f"Pesan dari pengguna ({update.effective_user.username}): {update.message.text}"

        # Mengirim pesan ke bot admin
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_message)

        # Menyampaikan bahwa pesan telah dikirim
        await update.message.reply_text("Pesan Anda telah dikirim ke admin. Mereka akan membalas segera.")
        return

    # Logika lain untuk menangani pesan pengguna
    await update.message.reply_text("Maaf, saya tidak mengerti. Silakan coba dengan kata kunci lain.")

# Fungsi untuk admin yang menerima pesan
async def handle_admin_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Di sini, admin dapat mengirim pesan ke pengguna
    user_chat_id = '5287460125'
    user_message = update.message.text

    # Mengirim balasan admin ke pengguna
    await context.bot.send_message(chat_id=user_chat_id, text=f"Admin menjawab: {user_message}")