import telepot
from telepot.loop import MessageLoop
import yaml
import message

with open('secret.yml', 'r', encoding='utf8') as f:
    secret = yaml.load(f, Loader=yaml.FullLoader)

# Telegram bot
BOT_TOKEN = secret['TELEGRAM_TOKEN']

bot = telepot.Bot(BOT_TOKEN)
MessageLoop(bot,message.message.handle_telegram_message).run_as_thread()
print('Listening for Telegram stickers...')

# Run the bot indefinitely
while True:
    pass
