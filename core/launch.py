import asyncio
import discord
import yaml



class launch():
    def launch_discord_bot(bot,chat_id,DISCORD_TOKEN,DISCORD_CHANNEL_ID):
        bot.sendChatAction(chat_id, 'upload_photo')
        intents = discord.Intents.all()
        intents.members = True
        client = discord.Client(intents=intents)
        sticker_file = discord.File('./media/sticker.gif')

        @client.event
        async def on_ready():
            try:
                channel = client.get_channel(DISCORD_CHANNEL_ID)
                await channel.typing()
                await channel.send(file=sticker_file)
                await client.close()
            except Exception as e:
                bot.sendMessage(chat_id, 'Error: Failed to send sticker to Discord. Please check the channel ID.')
                await client.close()
                
        client.run(DISCORD_TOKEN)