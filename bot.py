import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from groq import Groq

# Loglarni sozlash
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Environment o'zgaruvchilarini olish
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Groq mijozini sozlash
client = Groq(api_key=GROQ_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """/start buyrug'i uchun javob"""
    await context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Salom! Men Groq AI asosida ishlovchi aqlli botman. Menga xohlagan savolingizni bering!"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Foydalanuvchi xabarlarini qayta ishlash"""
    user_text = update.message.text
    
    try:
        # Groq AI ga so'rov yuborish
        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {"role": "system", "content": "Siz aqlli va foydali yordamchisiz. O'zbek tilida javob berasiz."},
                {"role": "user", "content": user_text}
            ],
            temperature=0.7,
            max_tokens=1024,
        )
        
        response_text = completion.choices[0].message.content
        await context.bot.send_message(chat_id=update.effective_chat.id, text=response_text)
        
    except Exception as e:
        logging.error(f"Xatolik yuz berdi: {e}")
        await context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text="Kechirasiz, javob qaytarishda xatolik yuz berdi. Keyinroq qayta urinib ko'ring."
        )

if __name__ == '__main__':
    # Botni ishga tushirish
    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    msg_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    
    application.add_handler(start_handler)
    application.add_handler(msg_handler)
    
    application.run_polling()
