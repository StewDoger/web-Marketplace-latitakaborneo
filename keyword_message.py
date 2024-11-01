import random
from telegram import Update
from telegram.ext import ContextTypes
from handlers import show_options, handle_lihat_produk, handle_cara_pembelian, handle_cara_bayar

# Respon produk detail
responses = {
    'akar bajakah': [
        "Halo Latier, untuk akar bajakah, beratnya 100g. Dikenal untuk meningkatkan kesehatan dan daya tahan tubuh. Cara penggunaannya dapat diseduh atau direbus. Apakah ada yang ingin kamu tanyakan lebih lanjut?",
        "Halo Latier, kami punya akar bajakah original dan yang sudah diracik. Mana yang kamu butuhkan? Apakah kamu ingin tahu lebih banyak tentang manfaatnya?",
        "Hai Latier, akar bajakah terkenal dengan banyak manfaat. Apakah kamu ingin tahu cara penggunaannya?",
        "Halo Latier, untuk akar bajakah, kami bisa bantu menjelaskan cara konsumsi dan dosis yang tepat."
    ],
    'pasak bumi': [
        "Halo Latier, berat Pasak Bumi adalah 50g dan saat ini tidak tersedia. Kami bisa rekomendasikan produk lain yang bermanfaat.",
        "Sayang sekali, Latier. Pasak Bumi saat ini tidak ready. Apakah kamu tertarik dengan produk herbal lainnya?",
        "Maaf, Latier. Pasak Bumi sedang habis. Kami punya alternatif lain yang bisa membantu kesehatanmu."
    ],
    'minyak uyut': [
        "Hallo Latier, Minyak Uyut kami beratnya 100ml dan efektif untuk mengurangi pegangan otot, keseleo, dan asma. Ingin tahu cara pemakaiannya?",
        "Halo Latier, berikut manfaat dari Minyak Uyut Latitaka: MENGURANGI PEGEL-PEGEL, KESELEO, ASMA, dan PERUT KEMBUNG. Ada yang ingin kamu tanyakan?",
        "Halo Latier, Minyak Uyut kami efektif untuk berbagai keluhan. Apakah ada informasi khusus yang kamu cari?"
    ],
    'madu': [
        "Hallo Latier, madu Latitaka memiliki berat 500ml dan kaya manfaat. Mau tahu lebih lanjut tentang khasiatnya?",
        "Halo Latier, kami memiliki madu alami yang sangat bermanfaat untuk kesehatan. Apakah ada yang ingin kamu ketahui?",
        "Hallo Latier, madu kami juga tersedia dalam berbagai varian rasa. Apakah kamu tertarik mencoba salah satunya?"
    ],
    'danum mea': [
        "Hallo Latier, Danum Mea beratnya 250gr/bungkus dan banyak dicari karena khasiatnya. Apakah kamu ingin informasi lebih lanjut?",
        "Halo Latier, kami sering merekomendasikan Danum Mea untuk kesehatan. Ada yang bisa kami bantu lebih lanjut?",
        "Hallo Latier, produk Danum Mea ini bagus untuk perawatan kesehatan. Mau tahu cara pengolahannya?"
    ],
    'nyaro nyerua': [
        "Hallo Latier, harga Nyaro Nyerua 1 pax/4 bungkus Rp. 150.000. Kami juga bisa menjelaskan manfaatnya.",
        "Halo Latier, Nyaro Nyerua sangat baik untuk kesehatan. Apakah kamu ingin tahu cara terbaik untuk mengonsumsinya?",
        "Hallo Latier, kami memiliki Nyaro Nyerua dengan banyak khasiat. Ada yang ingin kamu ketahui lebih lanjut?"
    ],
    'hampers': [
        "Hallo Latier, kami memiliki hampers menarik yang berisi berbagai produk kami. Apakah kamu ingin tahu isi dan harga hampers kami?",
        "Halo Latier, hampers Latitaka Borneo adalah pilihan sempurna untuk hadiah. Mau tahu lebih lanjut tentang pilihan hampers?",
        "Hallo Latier, kami bisa membuat hampers sesuai permintaan. Apa yang ingin kamu masukkan dalam hampers?"
    ],
    'pupur bosa': [
        "Hallo Latier, Pupur Bosa kami terbuat dari bahan alami dan banyak dicari. Ada yang ingin kamu tanyakan tentang manfaatnya?",
        "Halo Latier, Pupur Bosa cocok untuk perawatan wajah. Apakah kamu ingin tahu cara pemakaiannya?",
        "Hallo Latier, kami bisa menjelaskan khasiat Pupur Bosa untuk kecantikan. Mau tahu lebih banyak?"
    ],
    'minyak lengga unyut': [
        "Hallo Latier, Minyak Lengga Unyut kami sangat efektif untuk mengatasi berbagai keluhan. Beratnya 100ml. Apakah ada yang ingin kamu tanyakan?",
        "Halo Latier, Minyak Lengga Unyut dikenal untuk mengurangi nyeri otot. Ingin tahu cara penggunaannya?",
        "Hallo Latier, kami memiliki informasi lengkap tentang Minyak Lengga Unyut. Apakah kamu tertarik untuk mengetahuinya?"
    ],
    'akar dara': [
        "Hallo Latier, Akar Dara kami banyak digunakan dalam pengobatan tradisional. Beratnya 50g. Ada yang ingin kamu ketahui lebih lanjut?",
        "Halo Latier, kami punya Akar Dara dengan kualitas terbaik. Apakah kamu ingin tahu cara penggunaannya?",
        "Hallo Latier, Akar Dara dapat membantu menjaga kesehatan. Ingin tahu lebih banyak tentang manfaatnya?"
    ],
    'akar tampala': [
        "Hallo Latier, Akar Tampala terkenal karena manfaat kesehatannya. Beratnya 50g. Apakah ada informasi khusus yang kamu cari?",
        "Halo Latier, kami punya Akar Tampala yang berkualitas. Mau tahu lebih lanjut tentang produk ini?",
        "Hallo Latier, Akar Tampala sangat bermanfaat untuk kesehatan. Apakah kamu ingin tahu cara penggunaannya?"
    ],
    'kalawait': [
        "Hallo Latier, Kalawait adalah produk herbal yang bagus untuk kesehatan. Beratnya 100g. Ada yang ingin kamu ketahui?",
        "Halo Latier, kami menyediakan Kalawait yang berkualitas. Apakah kamu ingin informasi lebih lanjut?",
        "Hallo Latier, Kalawait memiliki banyak manfaat. Apakah kamu tertarik untuk mengetahui lebih banyak?"
    ],
    'racik latitaka': [
        "Hallo Latier, Racik Latitaka adalah campuran herbal terbaik untuk kesehatan. Ada yang ingin kamu tanyakan?",
        "Halo Latier, Racik Latitaka kami bisa disesuaikan dengan kebutuhan. Mau tahu lebih banyak?",
        "Hallo Latier, kami dapat menjelaskan khasiat Racik Latitaka. Apakah kamu tertarik untuk mengetahuinya?"
    ],
    'bawe bujangk': [
        "Hallo Latier, Bawe Bujangk memiliki khasiat yang sangat baik untuk kesehatan. Beratnya 100g. Apakah ada yang ingin kamu ketahui?",
        "Halo Latier, kami memiliki Bawe Bujangk dengan kualitas terbaik. Ingin tahu lebih lanjut tentang manfaatnya?",
        "Hallo Latier, Bawe Bujangk bisa membantu menjaga stamina. Mau tahu lebih banyak tentang cara penggunaannya?"
    ]
}

# Menambahkan respons untuk cara penggunaan
usage_responses = {
    'akar bajakah': [
        "Halo Latier, untuk akar bajakah, beratnya 100g. Dikenal untuk meningkatkan kesehatan dan daya tahan tubuh, serta dapat membantu dalam melawan sel kanker, mengurangi peradangan, dan meningkatkan sirkulasi darah. Apakah ada yang ingin kamu tanyakan lebih lanjut?",
        "Halo Latier, kami punya akar bajakah original dan yang sudah diracik. Akar bajakah juga dikenal untuk membantu mengobati diabetes, menjaga kesehatan ginjal, serta mengurangi stres oksidatif. Mana yang kamu butuhkan? Apakah kamu ingin tahu lebih banyak tentang manfaatnya?",
        "Hai Latier, akar bajakah terkenal dengan banyak manfaat, termasuk dalam meningkatkan sistem kekebalan tubuh dan mendetoksifikasi tubuh dari zat berbahaya. Apakah kamu ingin tahu cara penggunaannya?",
        "Halo Latier, untuk akar bajakah, kami bisa bantu menjelaskan cara konsumsi dan dosis yang tepat untuk manfaat kesehatan, seperti menurunkan tekanan darah dan kolesterol."
    ],
    'pasak bumi': [
        "Halo Latier, berat Pasak Bumi adalah 50g dan saat ini tidak tersedia. Pasak Bumi dikenal efektif untuk meningkatkan energi, libido, dan mengatasi masalah kesuburan. Kami bisa rekomendasikan produk lain yang bermanfaat.",
        "Sayang sekali, Latier. Pasak Bumi saat ini tidak ready. Tanaman ini banyak digunakan untuk pengobatan herbal dalam mengatasi kelelahan kronis dan menjaga keseimbangan hormon. Apakah kamu tertarik dengan produk herbal lainnya?",
        "Maaf, Latier. Pasak Bumi sedang habis. Kami punya alternatif lain yang bisa membantu kesehatanmu, seperti untuk memperbaiki kualitas tidur dan mengurangi stres."
    ],
    'minyak uyut': [
        "Hallo Latier, Minyak Uyut kami beratnya 100ml dan efektif untuk mengurangi pegangan otot, keseleo, asma, dan perut kembung. Ingin tahu cara pemakaiannya?",
        "Halo Latier, berikut manfaat dari Minyak Uyut Latitaka: MENGURANGI PEGEL-PEGEL, KESELEO, ASMA, dan PERUT KEMBUNG. Minyak ini juga baik untuk perawatan bagi penderita stroke ringan dan lumpuh akibat cedera otot. Ada yang ingin kamu tanyakan?",
        "Halo Latier, Minyak Uyut kami efektif untuk berbagai keluhan, termasuk mengatasi nyeri akibat radang sendi dan melemaskan otot yang tegang. Apakah ada informasi khusus yang kamu cari?"
    ],
    'madu': [
        "Hallo Latier, madu Latitaka memiliki berat 500ml dan kaya manfaat. Terutama baik untuk meningkatkan imunitas, memperbaiki pencernaan, serta meredakan batuk dan tenggorokan. Mau tahu lebih lanjut tentang khasiatnya?",
        "Halo Latier, kami memiliki madu alami yang sangat bermanfaat untuk kesehatan, seperti membantu mengatur kadar gula darah dan meningkatkan energi. Apakah ada yang ingin kamu ketahui?",
        "Hallo Latier, madu kami juga tersedia dalam berbagai varian rasa, masing-masing dengan khasiat berbeda seperti mengurangi risiko penyakit jantung dan mencegah kanker. Apakah kamu tertarik mencoba salah satunya?"
    ],
    'danum mea': [
        "Hallo Latier, Danum Mea beratnya 250gr/bungkus dan banyak dicari karena khasiatnya untuk melancarkan sirkulasi darah, menjaga kesehatan jantung, dan meningkatkan daya tahan tubuh. Apakah kamu ingin informasi lebih lanjut?",
        "Halo Latier, kami sering merekomendasikan Danum Mea untuk kesehatan, termasuk dalam perawatan pasien stroke, penderita kanker, dan untuk memperkuat sistem imun. Ada yang bisa kami bantu lebih lanjut?",
        "Hallo Latier, produk Danum Mea ini bagus untuk perawatan kesehatan terutama bagi penderita tumor dan untuk memperbaiki kualitas darah. Mau tahu cara pengolahannya?"
    ],
    'nyaro nyerua': [
        "Hallo Latier, harga Nyaro Nyerua 1 pax/4 bungkus Rp. 150.000. Nyaro Nyerua dikenal efektif untuk kondisi seperti asam urat, kolesterol, infeksi lambung, serta sebagai detoks alami. Kami juga bisa menjelaskan manfaatnya.",
        "Halo Latier, Nyaro Nyerua sangat baik untuk kesehatan, terutama bagi penderita diabetes, hipertensi, dan alergi. Apakah kamu ingin tahu cara terbaik untuk mengonsumsinya?",
        "Hallo Latier, kami memiliki Nyaro Nyerua dengan banyak khasiat, termasuk untuk mengatasi penyakit hati, menstabilkan kadar gula darah, dan menurunkan tekanan darah. Ada yang ingin kamu ketahui lebih lanjut?"
    ],
    'pupur bosa': [
        "Hallo Latier, Pupur Bosa kami terbuat dari bahan alami dan banyak dicari untuk perawatan kulit. Membantu merawat kulit wajah, mengurangi noda hitam, serta memperbaiki tekstur kulit. Ada yang ingin kamu tanyakan tentang manfaatnya?",
        "Halo Latier, Pupur Bosa cocok untuk perawatan wajah seperti mencegah jerawat dan memperbaiki jaringan kulit yang rusak. Apakah kamu ingin tahu cara pemakaiannya?",
        "Hallo Latier, kami bisa menjelaskan khasiat Pupur Bosa untuk kecantikan dan untuk menambah kecerahan alami kulit. Mau tahu lebih banyak?"
    ],
    'minyak lengga unyut': [
        "Minyak lengga unyut digunakan dengan cara mengoleskannya pada bagian yang membutuhkan, seperti otot yang pegal.",
        "Anda bisa mencampurkan minyak lengga unyut dengan minyak esensial lainnya untuk mendapatkan aroma yang lebih menyenangkan.",
        "Minyak ini juga dapat digunakan saat pijat untuk meningkatkan relaksasi."
    ],
    'akar dara': [
        "Akar dara bisa digunakan dengan cara direbus dalam air selama 20-30 menit dan diminum airnya untuk kesehatan.",
        "Anda juga dapat mengolah akar dara menjadi serbuk untuk dicampurkan ke dalam makanan.",
        "Konsumsi akar dara secara rutin untuk mendapatkan manfaat kesehatan yang lebih baik."
    ],
    'akar tampala': [
        "Akar tampala dapat direbus dan diminum airnya untuk mendapatkan manfaat kesehatannya.",
        "Anda bisa menambahkan akar tampala ke dalam makanan atau minuman sebagai bahan herbal.",
        "Gunakan akar tampala dengan cara yang sesuai untuk meningkatkan daya tahan tubuh."
    ],
    'kalawait': [
        "Kalawait dapat digunakan dengan cara direbus dan diminum airnya untuk mendapatkan khasiatnya.",
        "Anda juga dapat mencampurkan kalawait dengan bahan lain untuk meningkatkan manfaatnya.",
        "Kalawait bisa dimasak sebagai ramuan herbal yang baik untuk kesehatan."
    ],
    'racik latitaka': [
        "Racik Latitaka bisa digunakan dengan cara dicampurkan ke dalam air hangat atau makanan.",
        "Gunakan racik ini secara rutin untuk mendapatkan manfaat kesehatan secara optimal.",
        "Anda juga bisa menggunakan racik latitaka dalam bentuk kapsul sesuai dosis yang dianjurkan."
    ],
    'bawe bujangk': [
        "Bawe Bujangk dapat digunakan dengan cara direbus dan diminum airnya.",
        "Anda juga bisa mencampurkan bawe bujangk ke dalam makanan untuk menambah cita rasa dan manfaatnya.",
        "Konsumsi bawe bujangk secara rutin untuk kesehatan yang lebih baik."
    ]
}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text.lower()

    # Menangani salam
    if any(greet in user_message for greet in ['halo', 'hi', 'selamat pagi', 'selamat siang', 'selamat malam', 'hey', 'hai']):
        await update.message.reply_text("Halo Latier! Selamat datang di Latitaka Borneo. Apa yang bisa kami bantu hari ini?")
        await show_options(update, context)
        return

    # Menangani pertanyaan produk spesifik
    for product in responses.keys():
        if product in user_message:
            # Respons acak untuk produk yang relevan
            response = random.choice(responses[product])
            await update.message.reply_text(response)

            # Cek apakah pengguna menanyakan cara penggunaan
            if 'cara penggunaan' in user_message or 'cara pakai' in user_message:
                usage_response = random.choice(usage_responses[product])
                await update.message.reply_text(usage_response)
            return  # Stop processing further since we handled a valid product inquiry

    # Jika produk tidak dikenali, balas dengan pesan default
    await update.message.reply_text("Maaf, saya tidak mengerti. Apakah Anda ingin tahu tentang produk lain atau ada pertanyaan lainnya?")
    await show_options(update, context)

    # Specific inquiries
    if any(term in user_message for term in ['produk', 'daftar produk', 'lihat produk', 'tampilkan produk']):
        await handle_lihat_produk(update, context)
    elif any(term in user_message for term in ['cara beli', 'pembelian']):
        await handle_cara_pembelian(update, context)
    elif any(term in user_message for term in ['cara bayar', 'metode pembayaran']):
        await handle_cara_bayar(update, context)
    elif any(term in user_message for term in ['mau order', 'bisa order']):
        await update.message.reply_text("Halo Latier, Boleh bisa kami bantu ingin order apa?")

    # Closing message after handling a request
    elif any(term in user_message for term in ['terima kasih', 'makasih', 'thank you']):
        await update.message.reply_text("Sama-sama, Latier! Jika ada pertanyaan lain, jangan ragu untuk bertanya.")