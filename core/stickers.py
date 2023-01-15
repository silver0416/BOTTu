import os
import json
import requests
import launch
import pyrlottie 
from PIL import Image
import webp
import asyncio



class stickers():
    def handle_telegram_sticker(sticker_id,chat_id,bot,BOT_TOKEN,DISCORD_TOKEN,DISCORD_CHANNEL_ID):
        def FFMPEG():
            if os.name == 'nt':
                return True
            else:
                return False

        def imageMatting(path,background_color):
            image = Image.open(path)
            #get gif total frame
            total_frames =  image.n_frames
            duration = image.info['duration']
            print(duration)
            try:
                flag = 0
                while True:
                    if not os.path.exists("./media/pics/"):
                        os.mkdir("./media/pics/")
                    image.seek(flag) 
                    open("./media/pics/{}.png".format(flag),'a').close()
                    image.save("./media/pics/{}.png".format(flag))
                    pic = Image.open("./media/pics/{}.png".format(flag))
                    pic = pic.convert("RGBA")
                    color = pic.getpixel((0,0))
                    for i in range(pic.size[0]):
                        for j in range(pic.size[1]):
                            dot = (i,j)
                            rgba = pic.getpixel(dot)
                            if rgba == color:
                                rgba = rgba[:-1] + (0,)
                                pic.putpixel(dot, rgba)
                    pic.save("./media/pics/{}.png".format(flag))
                    flag +=1
                    print(flag)
            except BaseException as e:
                print(e)
            photo_list = []
            pic_list = os.listdir("./media/pics/")
            pic_list.sort(key=lambda x:int(x[:-4]))
            for k in pic_list:
                pic_p = Image.open("./media/pics/{}".format(k))
                photo_list.append(pic_p)
            photo_list[0].save("./media/sticker.gif", save_all=True, append_images=photo_list[1:],duration=duration,transparency=0,loop=0,disposal=3)
            for i in os.listdir("./media/pics/"):
                os.remove("./media/pics/{}".format(i))


        # Download the sticker
        r = requests.get('https://api.telegram.org/bot{}/getFile?file_id={}'.format(BOT_TOKEN, sticker_id), stream=True)
        if r.status_code != 200:
            print(f'Error: Failed to download sticker:{r.status_code}')
            print('https://api.telegram.org/bot{}/getFile?file_id={}'.format(BOT_TOKEN, sticker_id))
            return
        r = json.loads(r.text)
        file_path = r["result"]["file_path"]
        input_file_extension = file_path.split('.')[-1]

        r = requests.get('https://api.telegram.org/file/bot{}/{}'.format(BOT_TOKEN, file_path), stream=True)

        output_file_extension = input_file_extension

        if not os.path.exists(f'./media/sticker.{input_file_extension}'):
            open(f'./media/sticker.{input_file_extension}', 'a').close()
        with open(f'./media/sticker.{input_file_extension}', 'wb') as f:
            f.write(r.content)
        
        if input_file_extension == 'webp':
            print('webp')
            output_file_extension = 'png'
            if not os.path.exists('./media/sticker.png'):
                open('./media/sticker.png', 'a').close()
            image = webp.load_image("./media/sticker.webp").convert("RGBA")
            width, height = image.size
            n_width = 200
            ratio = float(n_width)/image.size[0]
            n_height = int(image.size[1]*ratio)
            r_image = image.resize((n_width,n_height), Image.ANTIALIAS)
            r_image.save("./media/sticker.png")

        
        elif input_file_extension == 'tgs':
            output_file_extension = 'gif'
            if not os.path.exists('./media/sticker.gif'):
                open('./media/sticker.gif', 'a').close()
            # Convert the sticker to gif
            tgs = pyrlottie.LottieFile("./media/sticker.tgs")
            async def convert():
                await pyrlottie.convSingleLottie(tgs,["./media/sticker.gif"],None,"010101")
            asyncio.run(convert())
            imageMatting("./media/sticker.gif","010101")
        
        else :
            output_file_extension = 'gif'
            if not os.path.exists('./media/sticker.gif'):
                open('./media/sticker.gif', 'a').close()
            # Convert the sticker to gif
            os.system('{} -i ./media/sticker.{} ./media/sticker.{} -y'.format(FFMPEG() and 'ffmpeg.exe' or 'ffmpeg',input_file_extension,output_file_extension))


        # Send the sticker to Discord
        launch.launch.launch_discord_bot(bot,chat_id,DISCORD_TOKEN,DISCORD_CHANNEL_ID,output_file_extension)