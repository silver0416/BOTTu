import os
import launch
from Log import log
import cv2

class gif():
    def handle_telegram_gif(sticker_id, chat_id, bot, BOT_TOKEN, DISCORD_TOKEN, DISCORD_CHANNEL_ID, OUTPUT_SIZE):
        # 使用 `get_file` 方法獲取貼圖文件信息
        file_info = bot.get_file(file_id=sticker_id) 
        # 從文件信息中提取文件路徑
        file_path = file_info.file_path  
        # 下載文件
        downloaded_file = bot.download_file(file_path)
        # 檢查 /media 和 /media/pics 目錄是否存在
        if not os.path.exists('./media'):
            os.mkdir('./media')
        if not os.path.exists('./media/pics'):
            os.mkdir('./media/pics')

        def OS():
            return os.name == 'nt'

        # 保存下載的 GIF 文件
        input_file_path = './media/input.gif'
        with open(input_file_path, 'wb') as f:
            f.write(downloaded_file)

        # 獲取 GIF 的幀率和尺寸
        video = cv2.VideoCapture(input_file_path)
        fps = video.get(cv2.CAP_PROP_FPS)
        original_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))

        # 設置輸出寬度
        if OUTPUT_SIZE == "original":
            n_width = original_width
        else:
            n_width = int(OUTPUT_SIZE)

        # 將 GIF 轉換為單獨的幀
        os.system('{} -i {} ./media/pics/frame%04d.png -y'.format(
            'ffmpeg.exe' if OS() else 'ffmpeg', input_file_path))

        # 使用 gifski 重新組合幀為 GIF
        output_file_path = './media/output.gif'
        os.system('{} --fps {} -W {} -o {} ./media/pics/frame*.png'.format(
            'gifski.exe' if OS() else 'gifski', fps, n_width, output_file_path))

        # 清理臨時文件
        for file in os.listdir("./media/pics/"):
            if file.endswith(".png"):
                os.remove(os.path.join("./media/pics/", file))

        # 發送 GIF 到 Discord
        launch.launch.launch_discord_bot(
            bot, chat_id, DISCORD_TOKEN, DISCORD_CHANNEL_ID, 'gif')

        # 刪除臨時 GIF 文件
        os.remove(input_file_path)
        os.remove(output_file_path)