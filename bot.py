import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters

TOKEN = os.getenv("TOKEN")

# ✅ MULTI ADMIN
ADMIN_IDS = ["5747624055", "1507609664"]

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

CHANNEL_USERNAME = "dark1544"

broadcast_mode = {}

# 🔹 Check join
async def is_joined(user_id, context):
    try:
        member = await context.bot.get_chat_member(f"@{CHANNEL_USERNAME}", user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

# 🔹 Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    ref = None
    if context.args:
        ref = context.args[0]

    if user_id not in users:
        users[user_id] = {"referrals": 0}

    joined = await is_joined(user_id, context)

    keyboard = [
        [InlineKeyboardButton("📢 Join Channel", url="https://t.me/dark1544")],
        [InlineKeyboardButton("📤 Invite Friends", url=f"https://t.me/share/url?url=https://t.me/CP_RP_BroSis_All_Videobot?start={user_id}")],
        [InlineKeyboardButton("✅ Check Join", callback_data=f"checkjoin_{ref}")],
        [InlineKeyboardButton("📊 Check Progress", callback_data="check")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if not joined:
        await update.message.reply_text(
            "👉 पहले 10 लोगो को channel join कराओ",
            reply_markup=reply_markup
        )
        return

    save_data(users)

    count = users[user_id]["referrals"]

    if count >= 10:
        text = """🎉 Congratulations!

✅ आपने 10 लोगों को invite कर दिया!

🔓 अब आपका access unlock हो गया है 👇

https://t.me/+f7oWI21E_JgzMzQ1
"""
    else:
        text = f"""👋 Welcome

👉 10 लोगो को invite करो + channel join कराओ तब आपको CP, RP और Bro Sis सभी Private Videos मिलेगा

👉 10 लोगो को invite करो + channel join जरूरी

🔗 Link:
https://t.me/CP_RP_BroSis_All_Videobot?start={user_id}

📊 Progress: {count}/10
"""

    await update.message.reply_text(text, reply_markup=reply_markup)

# 🔹 Button
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = str(query.from_user.id)
    data = query.data

    if data.startswith("checkjoin"):
        parts = data.split("_")
        ref = parts[1] if len(parts) > 1 else None

        joined = await is_joined(user_id, context)

        if not joined:
            await query.edit_message_text("❌ पहले channel join करो")
            return

        # ✅ referral count after join
        if ref and ref != user_id and ref in users:
            if "joined_users" not in users[ref]:
                users[ref]["joined_users"] = []

            if user_id not in users[ref]["joined_users"]:
                users[ref]["referrals"] += 1
                users[ref]["joined_users"].append(user_id)
                save_data(users)

        await query.edit_message_text("✅ Join verified! अब invite करो")
        return

    count = users.get(user_id, {}).get("referrals", 0)

    if count >= 10:
        msg = """🎉 Task Complete!

🔓 Videos यहाँ देखें:
https://t.me/+f7oWI21E_JgzMzQ1
"""
    else:
        msg = f"""📊 Progress: {count}/10

👉 10 लोगो को invite करो + channel join जरूरी
"""

    await query.edit_message_text(msg)

# 🔹 Admin panel
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_user.id) not in ADMIN_IDS:
        return

    keyboard = [
        [InlineKeyboardButton("📊 Stats", callback_data="stats")],
        [InlineKeyboardButton("📢 Broadcast", callback_data="broadcast")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("👑 Admin Panel", reply_markup=reply_markup)

# 🔹 Admin buttons
async def admin_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = str(query.from_user.id)

    if user_id not in ADMIN_IDS:
        return

    if query.data == "stats":
        total = len(users)
        await query.edit_message_text(f"👥 Total Users: {total}")

    elif query.data == "broadcast":
        broadcast_mode[user_id] = True
        await query.edit_message_text("📢 Message भेजो (सबको जाएगा)")

# 🔹 Broadcast
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    if user_id in broadcast_mode:
        msg = update.message.text
        sent = 0

        for uid in users:
            try:
                await context.bot.send_message(chat_id=uid, text=msg)
                sent += 1
            except:
                pass

        broadcast_mode.pop(user_id)
        await update.message.reply_text(f"✅ Broadcast sent to {sent} users")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("admin", admin))
app.add_handler(CallbackQueryHandler(button, pattern="^(check|checkjoin)"))
app.add_handler(CallbackQueryHandler(admin_buttons, pattern="^(stats|broadcast)"))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot Running...")
app.run_polling()
