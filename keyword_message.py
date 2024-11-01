import random
from telegram import Update
from telegram.ext import ContextTypes
from database import products_collection
from handlers import show_options, handle_lihat_produk, handle_cara_pembelian, handle_cara_bayar

# Respon produk detail
responses = {
    'akar bajakah': [
        "Halo Latier, untuk akar bajakah, beratnya 100g. Dikenal untuk meningkatkan kesehatan dan daya tahan tubuh. Cara penggunaannya dapat diseduh atau direbus.",
        "Halo Latier, kami punya akar bajakah original dan yang sudah diracik.",
        "Hai Latier, akar bajakah terkenal dengan banyak manfaat.",
        "Halo Latier, untuk akar bajakah, kami bisa bantu menjelaskan cara konsumsi dan dosis yang tepat."
    ],
    'pasak bumi': [
        "Halo Latier, berat Pasak Bumi adalah 50g dan saat ini tidak tersedia. Kami bisa rekomendasikan produk lain yang bermanfaat.",
        "Sayang sekali, Latier. Pasak Bumi saat ini tidak ready. Apakah kamu tertarik dengan produk herbal lainnya?",
        "Maaf, Latier. Pasak Bumi sedang habis. Kami punya alternatif lain yang bisa membantu kesehatanmu."
    ],
    'minyak uyut': [
        "Hallo Latier, Minyak Uyut kami beratnya 100ml dan efektif untuk mengurangi pegangan otot, keseleo, dan asma.",
        "Halo Latier, berikut manfaat dari Minyak Uyut Latitaka: MENGURANGI PEGEL-PEGEL, KESELEO, ASMA, dan PERUT KEMBUNG.",
        "Halo Latier, Minyak Uyut kami efektif untuk berbagai keluhan."
    ],
    'madu': [
        "Hallo Latier, madu Latitaka memiliki berat 500ml dan kaya manfaat.",
        "Halo Latier, kami memiliki madu alami yang sangat bermanfaat untuk kesehatan.",
        "Hallo Latier, madu kami juga tersedia dalam berbagai varian rasa."
    ],
    'danum mea': [
        "Hallo Latier, Danum Mea beratnya 250gr/bungkus dan banyak dicari karena khasiatnya.",
        "Halo Latier, kami sering merekomendasikan Danum Mea untuk kesehatan.",
        "Hallo Latier, produk Danum Mea ini bagus untuk perawatan kesehatan."
    ],
    'nyaro nyerua': [
        "Hallo Latier, harga Nyaro Nyerua 1 pax/4 bungkus Rp. 150.000. Kami juga bisa menjelaskan manfaatnya.",
        "Halo Latier, Nyaro Nyerua sangat baik untuk kesehatan.",
        "Hallo Latier, kami memiliki Nyaro Nyerua dengan banyak khasiat."
    ],
    'hampers': [
        "Hallo Latier, kami memiliki hampers menarik yang berisi berbagai produk kami.",
        "Halo Latier, hampers Latitaka Borneo adalah pilihan sempurna untuk hadiah.",
        "Hallo Latier, kami bisa membuat hampers sesuai permintaan."
    ],
    'pupur bosa': [
        "Hallo Latier, Pupur Bosa kami terbuat dari bahan alami dan banyak dicari.",
        "Halo Latier, Pupur Bosa cocok untuk perawatan wajah.",
        "Hallo Latier, kami bisa menjelaskan khasiat Pupur Bosa untuk kecantikan."
    ],
    'minyak lengga unyut': [
        "Hallo Latier, Minyak Lengga Unyut kami sangat efektif untuk mengatasi berbagai keluhan. Beratnya 100ml.",
        "Halo Latier, Minyak Lengga Unyut dikenal untuk mengurangi nyeri otot.",
        "Hallo Latier, kami memiliki informasi lengkap tentang Minyak Lengga Unyut."
    ],
    'akar dara': [
        "Hallo Latier, Akar Dara kami banyak digunakan dalam pengobatan tradisional. Beratnya 50g.",
        "Halo Latier, kami punya Akar Dara dengan kualitas terbaik.",
        "Hallo Latier, Akar Dara dapat membantu menjaga kesehatan."
    ],
    'akar tampala': [
        "Hallo Latier, Akar Tampala terkenal karena manfaat kesehatannya. Beratnya 50g.",
        "Halo Latier, kami punya Akar Tampala yang berkualitas.",
        "Hallo Latier, Akar Tampala sangat bermanfaat untuk kesehatan."
    ],
    'kalawait': [
        "Hallo Latier, Kalawait adalah produk herbal yang bagus untuk kesehatan. Beratnya 100g.",
        "Halo Latier, kami menyediakan Kalawait yang berkualitas.",
        "Hallo Latier, Kalawait memiliki banyak manfaat."
    ],
    'racik latitaka': [
        "Hallo Latier, Racik Latitaka adalah campuran herbal terbaik untuk kesehatan.",
        "Halo Latier, Racik Latitaka kami bisa disesuaikan dengan kebutuhan.",
        "Hallo Latier, kami dapat menjelaskan khasiat Racik Latitaka."
    ],
    'bawe bujangk': [
        "Hallo Latier, Bawe Bujangk memiliki khasiat yang sangat baik untuk kesehatan. Beratnya 100g.",
        "Halo Latier, kami memiliki Bawe Bujangk dengan kualitas terbaik.",
        "Hallo Latier, Bawe Bujangk bisa membantu menjaga stamina."
    ]
}

RESPONSE_MAP = {
    'produk': handle_lihat_produk,
    'cara beli': handle_cara_pembelian,
    'cara bayar': handle_cara_bayar
}

options_shown = False

async def handle_message(update, context):
    global options_shown  # Mengakses variabel global
    user_message = update.message.text.lower()

    # Respon untuk sapaan umum
    if any(greet in user_message for greet in ['halo', 'hi', 'selamat pagi', 'selamat siang', 'selamat malam', 'hey', 'hai']):
        await update.message.reply_text("Halo Latier! Selamat datang di Latitaka Borneo. Apa yang bisa kami bantu hari ini?")

        # Tampilkan opsi hanya jika belum ditampilkan
        if not options_shown:
            await show_options(update, context)
            options_shown = True  # Menandai bahwa opsi sudah ditampilkan
        return

    # Respon untuk permintaan produk atau daftar produk
    if any(term in user_message for term in ['produk', 'daftar produk', 'lihat produk', 'tampilkan produk']):
        await handle_lihat_produk(update, context)
        return

    # Respon untuk permintaan cara pembelian
    if 'cara beli' in user_message or 'pembelian' in user_message:
        await handle_cara_pembelian(update, context)
        return

    # Respon untuk permintaan cara pembayaran
    if 'cara bayar' in user_message or 'metode pembayaran' in user_message:
        await handle_cara_bayar(update, context)
        return

    # Respon untuk permintaan order dengan nama produk yang spesifik
    if any(term in user_message for term in ['mau order', 'bisa order', 'mau beli', 'beli', 'mau pesan', 'pesan']):
        matched_product = None
        try:
            products = products_collection.find({}, {"name": 1})  # Ambil hanya kolom 'name'
            for product in products:
                if product['name'].lower() in user_message:
                    matched_product = product['name']
                    break

            if matched_product:
                product_responses = responses.get(matched_product.lower())
                if product_responses:
                    response = random.choice(product_responses)
                    await update.message.reply_text(response)
                else:
                    await update.message.reply_text(f"Maaf, informasi lebih lanjut tentang {matched_product} belum tersedia.")
            else:
                await update.message.reply_text("Halo Latier, boleh kami bantu ingin produk apa?")
        except Exception as e:
            print(f"Error: {e}")
            await update.message.reply_text("Maaf, terjadi kesalahan saat memproses permintaan Anda. Silakan coba lagi nanti.")
        return

    # Respon untuk ucapan terima kasih
    if any(term in user_message for term in ['terima kasih', 'makasih', 'thank you']):
        await update.message.reply_text("Sama-sama, Latier! Jika ada pertanyaan lain, jangan ragu untuk bertanya.")
        return

    # Pengecekan untuk keyword produk yang terdapat di responses atau usage_responses
    for product, product_responses in responses.items():
        if product in user_message:
            response = random.choice(product_responses)
            await update.message.reply_text(response)
            return

    for product, usage_product_responses in responses.items():
        if product in user_message:
            response = random.choice(usage_product_responses)
            await update.message.reply_text(response)
            return

    # Jika tidak ada keyword yang dikenali, balas dengan pesan default
    await update.message.reply_text("Maaf, saya tidak mengerti. Apakah Anda ingin tahu tentang produk lain atau ada pertanyaan lainnya?")
    
    # Tampilkan opsi hanya jika belum ditampilkan
    if not options_shown:
        await show_options(update, context)
        options_shown = True  # Menandai bahwa opsi sudah ditampilkan