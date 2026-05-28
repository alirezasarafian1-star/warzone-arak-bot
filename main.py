from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import sqlite3
import random

TOKEN = "8464845224:AAE0zcoeFhaJcmLEaFORUG-CiDDRUqAjcgQ"

conn = sqlite3.connect("warzone.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS players(
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    money INTEGER,
    cups INTEGER,
    country TEXT
)
""")

conn.commit()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    cur.execute(
        "INSERT OR IGNORE INTO players VALUES(?,?,?,?,?)",
        (user.id, user.username, 5000, 100, "iran")
    )
    conn.commit()

    keyboard = [
        [InlineKeyboardButton("🏪 فروشگاه", callback_data="shop")],
        [InlineKeyboardButton("⚔️ حمله", callback_data="attack")],
        [InlineKeyboardButton("🏆 رنک جهانی", callback_data="top")],
        [InlineKeyboardButton("🌍 انتخاب کشور", callback_data="country")]
    ]

    await update.message.reply_text(
        "🔥 خوش اومدی سرباز اراک 🔥",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def top(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cur.execute("SELECT username, cups FROM players ORDER BY cups DESC LIMIT 10")
    rows = cur.fetchall()

    text = "🏆 رنک جهانی\n\n"
    for i, row in enumerate(rows, start=1):
        text += f"{i}. @{row[0]} - {row[1]} کاپ\n"

    await update.message.reply_text(text)

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "attack":
        cups = random.randint(5, 25)

        cur.execute(
            "UPDATE players SET cups=cups+?, money=money+500 WHERE user_id=?",
            (cups, query.from_user.id)
        )
        conn.commit()

        await query.message.reply_text(
            f"⚔️ حمله موفق\n🏆 +{cups} کاپ\n💰 +500 نیگرال"
        )

    elif query.data == "shop":
        await query.message.reply_text(
            "🏪 فروشگاه نظامی\n🚜 تانک\n🛸 پهباد\n🚀 موشک\n✈️ جنگنده"
        )

    elif query.data == "country":
        await query.message.reply_text(
            "🌍 کشورهای موجود:\n🇮🇷 ایران\n🇺🇸 آمریکا\n🇮🇱 اسرائیل"
        )

    elif query.data == "top":
        await top(update, context)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("top", top))
app.add_handler(CallbackQueryHandler(buttons))

print("WARZONE ARAK STARTED")

app.run_polling()
