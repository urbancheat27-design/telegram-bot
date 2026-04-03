import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

CHANNELS = ["@dark1544"]  # दूसरा channel बाद में add करेंगे

users = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    # Referral system
    if context.args:
        ref_id = int(context.args[0])
        if ref_id != user_id:
            users.setdefault(ref_id, {"ref": 0})
            users[ref_id]["ref"] += 1

    users.setdefault(user_id, {"ref": 0})

    ref_link = f"https://t.me/{context.bot.username}?start={user_id}"

    keyboard = [
        [InlineKeyboardButton("📢 Join Channel", url="https://t.me/dark1544")],
        [InlineKeyboardButton("✅ Verify Join", callback_data="check")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"👋 Welcome!\n\n"
        f"👥 Referrals: {users[user_id]['ref']}\n"
        f"🔗 Your Link:\n{ref_link}",
        reply_markup=reply_markup
    )

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    member = await context.bot.get_chat_member("@dark1544", user_id)

    if member.status in ["member", "administrator", "creator"]:
        await query.message.reply_text("✅ Verified! Sab task complete 🎉")
    else:
        await query.message.reply_text("❌ Pehle channel join karo!")

    await query.answer()

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(check))

print("🔥 2 Channel Bot chal raha hai...")

app.run_polling()
