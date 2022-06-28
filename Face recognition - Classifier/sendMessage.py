import telegram

TELEGRAM_BOT_TOKEN = '5535933470:AAFWP__W6-1fAxqrCQbE2QTXFDygnZhFnN8'
TELEGRAM_CHAT_ID = '-696427975'

bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="From Telegram Bot")

#bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=open(PHOTO_PATH, 'rb'))