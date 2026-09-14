import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Получаем ключи из переменных окружения (их мы добавим на Railway)
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
AITUNNEL_KEY = os.environ.get("DEEPSEEK_API_KEY")
BASE_URL = os.environ.get("DEEPSEEK_BASE_URL", "https://api.aitunnel.ru/v1")

# Настройка логов, чтобы видеть, что происходит
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.chat.send_action(action="typing")

    headers = {
        "Authorization": f"Bearer {AITUNNEL_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "Ты — мой личный помощник. Отвечай тепло, поддерживающе и по делу."},
            {"role": "user", "content": user_message}
        ]
    }

    try:
        response = requests.post(f"{BASE_URL}/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        bot_reply = result['choices'][0]['message']['content']
        await update.message.reply_text(bot_reply)
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        await update.message.reply_text("Прости, у меня сейчас проблемы с головой. Попробуй позже.")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # Бот будет отвечать на все текстовые сообщения
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Бот запущен и слушает...")
    application.run_polling()
