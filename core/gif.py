import os
import launch
from Log import log
import cv2
import requests

class gif():
    def handle_telegram_gif(file_id, chat_id, bot, BOT_TOKEN, DISCORD_TOKEN, DISCORD_CHANNEL_ID, OUTPUT_SIZE):
        # 下載 GIF 文件
        response = requests.get(
            f'https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}')
        if response.status_code != 200:
            log().info(f'Error: Failed to get file path: {response.status_code}')
            return
        file_info = response.json()
        file_path = file_info['result']['file_path']

        # 下載文件內容
        file_url = f'https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}'
        downloaded_file = requests.get(file_url).content
        # 檢查 /media 和 /media/pics 目錄是否存在
        if not os.path.exists('./media'):
            os.mkdir('./media')
        if not os.path.exists('./media/pics'):
            os.mkdir('./media/pics')

        with open('./media/sticker.mp4', 'wb') as f:
            f.write(downloaded_file)
        
        video = cv2.VideoCapture(f"./media/sticker.mp4")
        fps = video.get(cv2.CAP_PROP_FPS)
        log().info(f"FPS: {fps}")

        # 獲取視頻的寬度
        if OUTPUT_SIZE == "original":
            n_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        else:
            n_width = int(OUTPUT_SIZE)
        
        # 將視頻轉換為 GIF
        if fps > 50:  # GIF 的 FPS 限制為 50
            fps = 50
            os.system('{} -i ./media/sticker.mp4 -r 50 ./media/pics/frame%04d.png -y'.format(
                os.name == 'nt' and 'ffmpeg.exe' or 'ffmpeg'))
        else:
            os.system('{} -i ./media/sticker.mp4 -r {} ./media/pics/frame%04d.png -y'.format(
                os.name == 'nt' and 'ffmpeg.exe' or 'ffmpeg', fps))

        os.system('{} --fps {} -W {} -o ./media/sticker.gif ./media/pics/frame*.png'.format(
            os.name == 'nt' and 'gifski.exe' or 'gifski', fps, n_width))

        # 刪除所有 PNG 文件
        for i in os.listdir("./media/pics/"):
            if i.endswith(".png"):
                os.remove("./media/pics/{}".format(i))

        # 發送 GIF 到 Discord
        launch.launch.launch_discord_bot(
            bot, chat_id, DISCORD_TOKEN, DISCORD_CHANNEL_ID, 'gif')

