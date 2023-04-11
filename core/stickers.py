import os
import json
import requests
import launch
import pyrlottie
from PIL import Image
import webp
import asyncio
from PIL import Image
from Log import log
import cv2


class stickers():
    def handle_telegram_sticker(sticker_id, chat_id, bot, BOT_TOKEN, DISCORD_TOKEN, DISCORD_CHANNEL_ID, OUPUT_SIZE):
        # check if /media and /media/pics exist
        if not os.path.exists('./media'):
            os.mkdir('./media')
        if not os.path.exists('./media/pics'):
            os.mkdir('./media/pics')

        def OS():
            if os.name == 'nt':
                return True
            else:
                return False

        def imageMatting(path, width):
            msg_id = bot.sendMessage(chat_id, 'imageMatting: initializing, please wait...')[
                'message_id']
            log().info('imageMatting')
            gif = Image.open(path)
            total_frames = gif.n_frames
            fps = int(1000 / gif.info['duration'])
            log().info('fps: {}'.format(fps))

            # remove old files
            for i in os.listdir("./media/pics/"):
                if i.endswith(".png"):
                    os.remove("./media/pics/{}".format(i))

            os.system('{} -i {} ./media/pics/frame%04d.png -y'.format(OS()
                      and 'ffmpeg.exe' or 'ffmpeg', path))

            # imageMatting  for each frame
            n = 0
            for i in os.listdir("./media/pics/"):
                if i.endswith(".png"):
                    img = Image.open("./media/pics/{}".format(i))
                    img = img.convert("RGBA")
                    datas = img.getdata()
                    newData = []
                    for item in datas:
                        if item[0] == 1 and item[1] == 1 and item[2] == 1:
                            newData.append((0, 0, 0, 0))
                        else:
                            newData.append(item)
                    img.putdata(newData)
                    img.save("./media/pics/{}".format(i), "PNG")
                    bot.editMessageText((chat_id, msg_id), 'imageMatting: {}%, please wait...'.format(
                        round(n / total_frames * 100)))
                    n += 1
            bot.editMessageText((chat_id, msg_id), 'imageMatting: done')

            os.system('{} --fps {} -W {} -o ./media/sticker.gif ./media/pics/frame*.png'.format(
                OS() and 'gifski.exe' or 'gifski', fps, width))
            for i in os.listdir("./media/pics/"):
                os.remove("./media/pics/{}".format(i))

        # Download the sticker
        r = requests.get(
            'https://api.telegram.org/bot{}/getFile?file_id={}'.format(BOT_TOKEN, sticker_id), stream=True)
        if r.status_code != 200:
            log().info(f'Error: Failed to download sticker:{r.status_code}')
            log().info('https://api.telegram.org/bot{}/getFile?file_id={}'.format(BOT_TOKEN, sticker_id))
            return
        r = json.loads(r.text)
        file_path = r["result"]["file_path"]
        input_file_extension = file_path.split('.')[-1]

        r = requests.get(
            'https://api.telegram.org/file/bot{}/{}'.format(BOT_TOKEN, file_path), stream=True)

        output_file_extension = input_file_extension

        if not os.path.exists(f'./media/sticker.{input_file_extension}'):
            open(f'./media/sticker.{input_file_extension}', 'a').close()
        with open(f'./media/sticker.{input_file_extension}', 'wb') as f:
            f.write(r.content)

        if input_file_extension == 'webp':
            log().info('Converting webp to png')
            output_file_extension = 'png'
            if not os.path.exists('./media/sticker.png'):
                open('./media/sticker.png', 'a').close()
            image = webp.load_image("./media/sticker.webp").convert("RGBA")
            if OUPUT_SIZE == "original":
                image.save("./media/sticker.png")
            else:
                n_width = int(OUPUT_SIZE)
                ratio = float(n_width)/image.size[0]
                n_height = int(image.size[1]*ratio)
                r_image = image.resize((n_width, n_height), Image.ANTIALIAS)
                r_image.save("./media/sticker.png")

        elif input_file_extension == 'tgs':
            log().info('Converting tgs to gif')
            output_file_extension = 'gif'
            if not os.path.exists('./media/sticker.gif'):
                open('./media/sticker.gif', 'a').close()
            # Convert the sticker to gif
            tgs = pyrlottie.LottieFile("./media/sticker.tgs")
            # if pyrlottie show permission denied in linux, run this command in terminal: sudo chmod +x /PYTHON_PATH/site-packages/pyrlottie/linux_x86_64/lottie2gif

            async def convert():
                await pyrlottie.convSingleLottie(tgs, ["./media/sticker.gif"], None, "010101")
            asyncio.run(convert())
            if OUPUT_SIZE == "original":
                n_width = Image.open("./media/sticker.gif").size[0]
            else:
                n_width = int(OUPUT_SIZE)
            imageMatting("./media/sticker.gif", n_width)

        else:
            log().info('Converting {} to gif'.format(input_file_extension))
            output_file_extension = 'gif'
            if not os.path.exists('./media/sticker.gif'):
                open('./media/sticker.gif', 'a').close()
            # Get the fps of the sticker
            video = cv2.VideoCapture(f"./media/sticker.{input_file_extension}")
            fps = video.get(cv2.CAP_PROP_FPS)

            # width
            if OUPUT_SIZE == "original":
                n_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
            else:
                n_width = int(OUPUT_SIZE)
            # Convert the sticker to gif

            if fps > 50:  # gif fps limit is 50
                fps = 50
                os.system('{} -i ./media/sticker.{} -r 50 ./media/pics/frame%04d.png -y'.format(
                    OS() and 'ffmpeg.exe' or 'ffmpeg', input_file_extension))
            else:
                os.system('{} -i ./media/sticker.{} ./media/pics/frame%04d.png -y'.format(
                    OS() and 'ffmpeg.exe' or 'ffmpeg', input_file_extension))

            os.system('{} --fps {} -W {} -o ./media/sticker.{} ./media/pics/frame*.png'.format(
                OS() and 'gifski.exe' or 'gifski', fps, n_width, output_file_extension))

            # remove all the png files in the folder
            for i in os.listdir("./media/pics/"):
                if i.endswith(".png"):
                    os.remove("./media/pics/{}".format(i))

        # Send the sticker to Discord
        launch.launch.launch_discord_bot(
            bot, chat_id, DISCORD_TOKEN, DISCORD_CHANNEL_ID, output_file_extension)
