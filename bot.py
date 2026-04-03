import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 Join Channel", url="https://t.me/yourchannel")],
        [InlineKeyboardButton("✅ Check", callback_data="check")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Join karke check karo", reply_markup=reply_markup)

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("✅ Bot 24x7 chal raha hai 🎉")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(check))

app.run_polling()
