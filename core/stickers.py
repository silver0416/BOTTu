import os
import json
import requests
import launch


class stickers():
    def handle_telegram_sticker(sticker_id,chat_id,bot,BOT_TOKEN,DISCORD_TOKEN,DISCORD_CHANNEL_ID):
        def FFMPEG():
            if os.name == 'nt':
                return True
            else:
                return False
        # Download the sticker
        r = requests.get('https://api.telegram.org/bot{}/getFile?file_id={}'.format(BOT_TOKEN, sticker_id), stream=True)
        if r.status_code != 200:
            print(f'Error: Failed to download sticker:{r.status_code}')
            print('https://api.telegram.org/bot{}/getFile?file_id={}'.format(BOT_TOKEN, sticker_id))
            return
        r = json.loads(r.text)
        file_path = r["result"]["file_path"]
        r = requests.get('https://api.telegram.org/file/bot{}/{}'.format(BOT_TOKEN, file_path), stream=True)

        if not os.path.exists('./media/sticker.webp'):
            open('./media/sticker.webp', 'a').close()
        with open('./media/sticker.webp', 'wb') as f:
            f.write(r.content) 

        if not os.path.exists('./media/sticker.gif'):
            open('./media/sticker.gif', 'a').close()
        # Convert the sticker to gif
        os.system('{} -i ./media/sticker.webp ./media/sticker.gif -y'.format(FFMPEG() and 'ffmpeg.exe' or 'ffmpeg'))

        # Send the sticker to Discord
        launch.launch.launch_discord_bot(bot,chat_id,DISCORD_TOKEN,DISCORD_CHANNEL_ID)