import telepot
from telepot.loop import MessageLoop
import yaml
import message
from Log import log

log().start()
with open('secret.yml', 'r', encoding='utf8') as f:
    secret = yaml.load(f, Loader=yaml.FullLoader)

# Telegram bot
BOT_TOKEN = secret['TELEGRAM_TOKEN']

bot = telepot.Bot(BOT_TOKEN)
MessageLoop(bot, {'chat': message.message.handle_telegram_message,
            'callback_query': message.message.on_callback_query}).run_forever()
log().info('Telegram bot started.')