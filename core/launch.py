import discord
from Log import log


class launch():
    def launch_discord_bot(bot,chat_id,DISCORD_TOKEN,DISCORD_CHANNEL_ID,output_file_extension):
        bot.sendChatAction(chat_id, 'upload_photo')
        intents = discord.Intents.all()
        intents.members = True
        client = discord.Client(intents=intents)
        sticker_file = discord.File(f'./media/sticker.{output_file_extension}')

        @client.event
        async def on_ready():
            try:
                channel = client.get_channel(DISCORD_CHANNEL_ID)
                log().info(f"Sending sticker to Discord channel: {channel}")
                await channel.typing()
                await channel.send(file=sticker_file)
                log().info("Sticker sent to Discord.")
                await client.close()
            except Exception as e:
                log().log("Error: Failed to send sticker to Discord. Please check the channel ID.")
                bot.sendMessage(chat_id, 'Error: Failed to send sticker to Discord. Please check the channel ID.')
                await client.close()
                
        client.run(DISCORD_TOKEN)