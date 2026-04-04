import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

TOKEN = os.getenv("TOKEN")

DATA_FILE = "data.json"

def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

users = load_data()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    ref = None
    if context.args:
        ref = context.args[0]

    if user_id not in users:
        users[user_id] = {"referrals": 0}

        if ref and ref != user_id and ref in users:
            users[ref]["referrals"] += 1

    save_data(users)

    count = users[user_id]["referrals"]

    # 🔘 Buttons
    keyboard = [
        [InlineKeyboardButton("📢 Join Channel", url="https://t.me/dark1544")],
        [InlineKeyboardButton("📤 Invite Friends", url=f"https://t.me/share/url?url=https://t.me/CP_RP_BroSis_All_Videobot?start={user_id}")],
        [InlineKeyboardButton("📊 Check Progress", callback_data="check")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if count >= 10:
        text = """🎉 Congratulations!

✅ आपने 10 लोगों को invite कर दिया!

🔓 अब आपका access unlock हो गया है 👇

https://t.me/+f7oWI21E_JgzMzQ1
"""
    else:
        text = f"""👋 Welcome

👉 10 लोगो को invite करो तब आपको CP, RP और Bro Sis Private Videos मिलेगा 🔗

🔗 Link:
https://t.me/CP_RP_BroSis_All_Videobot?start={user_id}

📊 Progress: {count}/10
"""

    await update.message.reply_text(text, reply_markup=reply_markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = str(query.from_user.id)
    count = users.get(user_id, {}).get("referrals", 0)

    if count >= 10:
        msg = """🎉 Task Complete!

🔓 अब videos यहाँ देखें:
https://t.me/+f7oWI21E_JgzMzQ1
"""
    else:
        msg = f"""📊 Progress: {count}/10

👉 10 लोगो को invite करो तब आपको CP, RP और Bro Sis Private Videos मिलेगा
"""

    await query.edit_message_text(msg)


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

print("Bot Running...")
app.run_polling()
