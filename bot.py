import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TOKEN")
CHANNEL = "@dark1544"

users = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    # Referral system
    if context.args:
        ref_id = int(context.args[0])
        if ref_id != user_id:
            users.setdefault(ref_id, {"ref": 0})
            users[ref_id]["ref"] += 1

    users.setdefault(user_id, {"ref": 0, "verified": False, "shared": False})

    ref_link = f"https://t.me/{context.bot.username}?start={user_id}"

    keyboard = [
        [InlineKeyboardButton("📢 Join Channel", url="https://t.me/dark1544")],
        [InlineKeyboardButton("✅ Verify Join", callback_data="verify")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"👋 Welcome!\n\n"
        f"👥 Referrals: {users[user_id]['ref']}\n"
        f"🔗 Your Link:\n{ref_link}\n\n"
        f"👉 Step 1: Channel join karo",
        reply_markup=reply_markup
    )

async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    member = await context.bot.get_chat_member(CHANNEL, user_id)

    if member.status in ["member", "administrator", "creator"]:
        users[user_id]["verified"] = True

        keyboard = [
            [InlineKeyboardButton("📤 Share to 5 Friends", url="https://t.me/share/url?url=https://t.me/dark1544")],
            [InlineKeyboardButton("✅ Done Sharing", callback_data="share_done")]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_text(
            "✅ Channel join ho gaya!\n\n👉 Ab channel ko 5 logo ko share karo",
            reply_markup=reply_markup
        )
    else:
        await query.message.reply_text("❌ Pehle channel join karo!")

    await query.answer()

async def share_done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    if users[user_id]["verified"]:
        users[user_id]["shared"] = True
        await query.message.reply_text("🎉 Sab task complete! Ab aap videos dekh sakte ho 😎")
    else:
        await query.message.reply_text("❌ Pehle join verify karo!")

    await query.answer()

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(verify, pattern="verify"))
app.add_handler(CallbackQueryHandler(share_done, pattern="share_done"))

print("🔥 Pro Bot chal raha hai...")

app.run_polling()
