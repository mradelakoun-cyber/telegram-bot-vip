import asyncio
import json
import random
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# ================= CONFIG =================
API_TOKEN = "8615451117:AAHThlA55fYeK3WpHGcs1-K0KBwnYrDFvbM"
ADMIN_ID = 8364685971

# 📌 vidéo sauvegardée automatiquement ici
VIDEO_FILE_ID = None

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# ================= SAVE VIDEO =================
@dp.message(lambda m: m.video)
async def save_video(message: types.Message):
    global VIDEO_FILE_ID
    VIDEO_FILE_ID = message.video.file_id
    await message.answer("✅ Vidéo enregistrée avec succès")

# ================= USERS =================
try:
    with open("users.json", "r") as f:
        users = json.load(f)
except:
    users = {}

def save_users():
    with open("users.json", "w") as f:
        json.dump(users, f)

# ================= MENU =================
menu = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text="📡 SIGNAL"), types.KeyboardButton(text="📊 STATUT")],
        [types.KeyboardButton(text="🔐 Activer VIP")]
    ],
    resize_keyboard=True
)

# ================= START =================
@dp.message(CommandStart())
async def start(message: types.Message):
    user_id = str(message.from_user.id)

    if user_id not in users:
        users[user_id] = {"vip": False, "step": None, "last_signal": None}

    save_users()
    await message.answer("🚀 BOT VIP ACTIF", reply_markup=menu)

# ================= SIGNAL =================
def ai_engine():
    return random.randint(30, 55)

@dp.message(lambda m: m.text == "📡 SIGNAL")
async def signal(message: types.Message):
    user_id = str(message.from_user.id)

    if user_id not in users or not users[user_id].get("vip"):
        await message.answer("🔒 VIP requis")
        return

    if not VIDEO_FILE_ID:
        await message.answer("❌ Aucune vidéo enregistrée")
        return

    score = ai_engine()

    if score >= 50:
        target = round(random.uniform(6, 18), 2)
    elif score >= 40:
        target = round(random.uniform(3, 8), 2)
    else:
        target = round(random.uniform(1.5, 4), 2)

    safe = round(random.uniform(1.3, 2.2), 2)
    time_str = (datetime.now() + timedelta(minutes=2)).strftime("%H:%M")

    text = f"""🚀 PREDICTION LUCKY JET

📡 SIGNAL: {time_str}

🎯 Objectif: jusqu'à {target}X
🛡️ SECURITÉ: {safe}X
"""

    await bot.send_video(
        message.chat.id,
        VIDEO_FILE_ID,
        caption=text
    )

# ================= STATUT =================
@dp.message(lambda m: m.text == "📊 STATUT")
async def status(message: types.Message):
    user_id = str(message.from_user.id)

    if user_id in users and users[user_id].get("vip"):
        await message.answer("✅ VIP ACTIF")
    else:
        await message.answer("❌ NON VIP")

# ================= RUN =================
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())