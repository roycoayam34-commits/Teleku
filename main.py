import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)

TOKEN = os.getenv("BOT_TOKEN")

# ===== /info =====
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Halo 👋\n\n"
        "Selamat datang di bot layanan kami.\n"
        "Ketik /pricelist untuk lihat harga\n"
        "Ketik /isi_form untuk order."
    )

# ===== /pricelist =====
async def pricelist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_photo(
        photo=open("pricelist.jpg", "rb"),
        caption="Daftar harga kami 📋"
    )

# ===== FORM =====
NAMA, ALAMAT, PESANAN = range(3)

async def isi_form(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Masukkan nama kamu:")
    return NAMA

async def nama(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["nama"] = update.message.text
    await update.message.reply_text("Masukkan alamat:")
    return ALAMAT

async def alamat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["alamat"] = update.message.text
    await update.message.reply_text("Pesanan kamu apa?")
    return PESANAN

async def pesanan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["pesanan"] = update.message.text

    hasil = f"""
📩 ORDER MASUK

Nama: {context.user_data['nama']}
Alamat: {context.user_data['alamat']}
Pesanan: {context.user_data['pesanan']}
"""

    # GANTI DENGAN ID TELEGRAM KAMU
    await context.bot.send_message(chat_id=6902689922, text=hasil)

    await update.message.reply_text("Pesanan sudah kami terima ✅")
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("pricelist", pricelist))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("isi_form", isi_form)],
        states={
            NAMA: [MessageHandler(filters.TEXT & ~filters.COM
