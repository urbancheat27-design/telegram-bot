import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters

TOKEN = os.getenv("TOKEN")

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

# ✅ TWO CHANNELS
CHANNELS = ["dark1544", "+lRKxuCwsiJ02N2Fl"]
broadcast_mode = {}

# 🔹 Check join (BOTH channels)
async def is_joined(user_id, context):
    try:
        for ch in CHANNELS:
            member = await context.bot.get_chat_member(f"@{ch}", user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        return True
    except:
        return False

# 🔹 Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    ref = context.args[0] if context.args else None

    if user_id not in users:
        users[user_id] = {"referrals": 0, "joined_users": []}

    joined = await is_joined(user_id, context)

    # 🔥 Invite message with BOTH links (clickable)
    invite_text = f"""🔥 Free Private Videos पाने के लिए 👇

1️⃣ Bot Start करो:
https://t.me/CP_RP_BroSis_All_Videobot?start={user_id}

2️⃣ इन दोनों channels को join करो:
https://t.me/dark1544
https://t.me/+lRKxuCwsiJ02N2Fl

👉 Join करके "Check Join" दबाओ
"""

    keyboard = [
        [InlineKeyboardButton("📢 Join Channel 1", url="https://t.me/dark1544")],
        [InlineKeyboardButton("📢 Join Channel 2", url="https://t.me/+lRKxuCwsiJ02N2Fl")],
        [InlineKeyboardButton("📤 Invite Friends", url=f"https://t.me/share/url?text={invite_text}")],
        [InlineKeyboardButton("✅ Check Join", callback_data=f"checkjoin_{ref}")],
        [InlineKeyboardButton("📊 Check Progress", callback_data="check")]
    ]

    if not joined:
        await update.message.reply_text(
            "👉 पहले 10 लोगो को दोनों channel join कराओ",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    save_data(users)

    count = users[user_id]["referrals"]

    if count >= 10:
        text = f"""🎉 Congratulations!

🔓 आपने 10 लोगो को successfully join करवा दिया!

👉 Videos यहाँ देखें:
https://t.me/+f7oWI21E_JgzMzQ1
"""
    else:
        text = f"""👋 Welcome

👉 10 लोगो को invite करो + दोनों channel join कराओ तब आपको CP, RP और Bro Sis सभी Private Videos मिलेगा

👉 10 लोगो को invite करो + channel join जरूरी

🔗 आपका लिंक:
https://t.me/CP_RP_BroSis_All_Videobot?start={user_id}

📊 Progress: {count}/10
"""

    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

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
            await query.edit_message_text("❌ दोनों channel join करो")
            return

        # Referral count after join
        if ref and ref != user_id and ref in users:
            if user_id not in users[ref]["joined_users"]:
                users[ref]["referrals"] += 1
                users[ref]["joined_users"].append(user_id)
                save_data(users)

                # 🔥 AUTO UNLOCK
                if users[ref]["referrals"] >= 10:
                    try:
                        await context.bot.send_message(
                            chat_id=ref,
                            text=f"""🎉 Congratulations!

🔓 10 लोग join करवा दिए!

👉 Videos:
https://t.me/+f7oWI21E_JgzMzQ1
"""
                        )
                    except:
                        pass

        await query.edit_message_text("✅ Join verified! अब invite करो")
        return

    count = users.get(user_id, {}).get("referrals", 0)

    if count >= 10:
        msg = """🎉 Task Complete!

🔓 Videos:
https://t.me/+f7oWI21E_JgzMzQ1
"""
    else:
        msg = f"📊 Progress: {count}/10"

    await query.edit_message_text(msg)

# 🔹 Admin
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_user.id) not in ADMIN_IDS:
        return

    keyboard = [
        [InlineKeyboardButton("📊 Stats", callback_data="stats")],
        [InlineKeyboardButton("📢 Broadcast", callback_data="broadcast")]
    ]

    await update.message.reply_text("👑 Admin Panel", reply_markup=InlineKeyboardMarkup(keyboard))

# 🔹 Admin buttons
async def admin_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = str(query.from_user.id)

    if user_id not in ADMIN_IDS:
        return

    if query.data == "stats":
        await query.edit_message_text(f"👥 Total Users: {len(users)}")

    elif query.data == "broadcast":
        broadcast_mode[user_id] = True
        await query.edit_message_text("📢 Message भेजो")

# 🔹 Broadcast
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    if user_id in broadcast_mode:
        msg = update.message.text
        for uid in users:
            try:
                await context.bot.send_message(chat_id=uid, text=msg)
            except:
                pass

        broadcast_mode.pop(user_id)
        await update.message.reply_text("✅ Broadcast done")

# 🔹 App init
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("admin", admin))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(CallbackQueryHandler(admin_buttons))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot Running...")
app.run_polling()
