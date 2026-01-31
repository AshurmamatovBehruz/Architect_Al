import os
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters
from google import genai

# 🔑 Token va API kalit
TOKEN = os.getenv("TELEGRAM_TOKEN")
API_KEY = os.getenv("GEMINI_API_KEY")
ADMIN_ID = int(os.getenv("ADMIN_ID", "6325359052"))  # Admin ID ni Railway Variables’da qo‘shing

# 🤖 Gemini client
client = genai.Client(api_key=API_KEY)

# 🧠 Memory
user_memory = {}
known_users = set()

SYSTEM_PROMPT = "You are Architect AI, an assistant for architecture and design."

# 🔍 Oddiy til aniqlash (lotin harflariga mos)
def detect_language(text: str) -> str:
    # Agar matnda o‘zbekcha so‘zlar bo‘lsa, "uz" qaytaradi
    uzbek_keywords = ["salom", "rahmat", "qayer", "uy", "loyiha", "me'mor"]
    if any(word in text.lower() for word in uzbek_keywords):
        return "uz"
    return "en"

# 📩 Xabarlarni qayta ishlash
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id
    username = user.username or "no_username"
    name = user.first_name or "unknown"
    user_text = update.message.text

    # 🔔 Admin xabari (faqat yangi user)
    if user_id not in known_users:
        known_users.add(user_id)
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"🆕 Yangi user botga yozdi: @{username} | {name} | ID: {user_id}"
        )

    # 🧠 Memory
    if user_id not in user_memory:
        user_memory[user_id] = []

    user_memory[user_id].append(f"User: {user_text}")

    lang = detect_language(user_text)
    lang_instruction = "Answer in Uzbek." if lang == "uz" else "Answer in English."

    prompt = (
        SYSTEM_PROMPT
        + "\n"
        + lang_instruction
        + "\n"
        + "\n".join(user_memory[user_id][-6:])
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",   # Flash modeli — tez va arzon
        contents=prompt
    )

    reply = response.candidates[0].content.parts[0].text
    user_memory[user_id].append(f"Architect AI: {reply}")

    await update.message.reply_text(reply)

# 🚀 Botni ishga tushirish
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Architect AI Bot ishlayapti...")
    app.run_polling()

if __name__ == "__main__":
    main()
