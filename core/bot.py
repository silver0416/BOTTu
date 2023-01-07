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
FFMPEG_PATH = 'ffmpeg'

def handle_telegram_sticker(sticker_id,chat_id):
    # Download the sticker
    r = requests.get('https://api.telegram.org/bot{}/getFile?file_id={}'.format(BOT_TOKEN, sticker_id), stream=True)
    if r.status_code != 200:
        print(f'Error: Failed to download sticker:{r.status_code}')
        print('https://api.telegram.org/bot{}/getFile?file_id={}'.format(BOT_TOKEN, sticker_id))
        return
    r = json.loads(r.text)
    file_path = r["result"]["file_path"]
    r = requests.get('https://api.telegram.org/file/bot{}/{}'.format(BOT_TOKEN, file_path), stream=True)

    with open('./media/sticker.webp', 'wb') as f:
        f.write(r.content) 

    # Convert the sticker to gif
    os.system('{} -i ./media/sticker.webp ./media/sticker.gif -y'.format(FFMPEG_PATH))

    # Send the gif to Discord
    intents = discord.Intents.all()
    intents.members = True
    client = discord.Client(intents=intents)
    sticker_file = discord.File('./media/sticker.gif')

    @client.event
    async def on_ready():
        try:
            channel = client.get_channel(DISCORD_CHANNEL_ID)
            await channel.send(file=sticker_file)
            await client.close()
        except Exception as e:
            bot.sendMessage(chat_id, 'Error: Failed to send sticker to Discord. Please check the channel ID.')
            await client.close()
            
    client.run(DISCORD_TOKEN)

def handle_telegram_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'sticker':
        handle_telegram_sticker(msg['sticker']['file_id'],chat_id)
    elif content_type == 'text':
        command = msg['text'].split()[0]
        if command == '/start':
            bot.sendMessage(chat_id, 'Hello! I am a sticker bot. Send me a sticker and I will send it to Discord.\n'+
                                        'send /set to set the Discord channel id to send the sticker to.\n'+
                                        'send /nowID to get the current Discord channel id.')
        elif command == '/set':
            if len(msg['text'].split()) != 2:
                bot.sendMessage(chat_id, 'Error: Invalid command. Please send /set DISCORD_CHANNEL_ID')
                return
            global DISCORD_CHANNEL_ID 
            DISCORD_CHANNEL_ID = int(msg['text'].split()[1])
            bot.sendMessage(chat_id, 'Discord channel ID set to {}'.format(DISCORD_CHANNEL_ID))
        elif command == '/nowID':
            bot.sendMessage(chat_id, 'Current Discord channel ID is {}'.format(DISCORD_CHANNEL_ID))
        else:
            bot.sendMessage(chat_id, 'I only accept stickers.')

# Set up the Telegram bot
bot = telepot.Bot(BOT_TOKEN)
MessageLoop(bot, handle_telegram_message).run_as_thread()
print('Listening for Telegram stickers...')

# Run the bot indefinitely
while True:
    pass
