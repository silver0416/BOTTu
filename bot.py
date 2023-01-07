import json
import os
import requests
import telepot
from telepot.loop import MessageLoop
import discord
import yaml

with open('secret.yml', 'r', encoding='utf8') as f:
    secret = yaml.load(f, Loader=yaml.FullLoader)

# Telegram bot
BOT_TOKEN = secret['TELEGRAM_TOKEN']

# Discord bot
DISCORD_TOKEN = secret['DISCORD_TOKEN']
DISCORD_CHANNEL_ID = secret['DISCORD_CHANNEL_ID']

# ffmpeg path
FFMPEG_PATH = 'ffmpeg.exe'

def handle_telegram_sticker(sticker_id):
    # Download the sticker
    r = requests.get('https://api.telegram.org/bot{}/getFile?file_id={}'.format(BOT_TOKEN, sticker_id), stream=True)
    if r.status_code != 200:
        print(f'Error: Failed to download sticker:{r.status_code}')
        print('https://api.telegram.org/bot{}/getFile?file_id={}'.format(BOT_TOKEN, sticker_id))
        return
    r = json.loads(r.text)
    file_path = r["result"]["file_path"]
    r = requests.get('https://api.telegram.org/file/bot{}/{}'.format(BOT_TOKEN, file_path), stream=True)

    with open('sticker.webp', 'wb') as f:
        f.write(r.content)

    # Convert the sticker to gif
    os.system('{} -i sticker.webp sticker.gif -y'.format(FFMPEG_PATH))

    # Send the gif to Discord
    intents = discord.Intents.all()
    intents.members = True
    client = discord.Client(intents=intents)
    sticker_file = discord.File('sticker.gif')

    @client.event
    async def on_ready():
        channel = client.get_channel(DISCORD_CHANNEL_ID)
        await channel.send(file=sticker_file)
        await client.close()
    client.run(DISCORD_TOKEN)

def handle_telegram_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'sticker':
        handle_telegram_sticker(msg['sticker']['file_id'])

# Set up the Telegram bot
bot = telepot.Bot(BOT_TOKEN)
MessageLoop(bot, handle_telegram_message).run_as_thread()
print('Listening for Telegram stickers...')

# Run the bot indefinitely
while True:
    pass
