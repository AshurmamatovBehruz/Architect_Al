import os
import google.genai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# 🔐 KALITLARNI TIZIMDAN OLAMIZ
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Gemini sozlash
client = genai.Client(api_key=GEMINI_API_KEY)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_text
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text("Xatolik yuz berdi 😕")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Architect AI Bot ishlayapti...")
    app.run_polling()

if __name__ == "__main__":
    main()


