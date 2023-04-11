import telepot
import yaml
import stickers
from Log import log


with open('secret.yml', 'r', encoding='utf8') as f:
    secret = yaml.load(f, Loader=yaml.FullLoader)
with open('config.yml', 'r', encoding='utf8') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)


# Telegram bot
BOT_TOKEN = secret['TELEGRAM_TOKEN']
DISCORD_TOKEN = secret['DISCORD_TOKEN']
DISCORD_CHANNEL_ID = secret['DISCORD_CHANNEL_ID']

OUTPUT_SIZE, DEFAULT_OUTPUT_SIZE = config['OUTPUT_SIZE'] , config['OUTPUT_SIZE']

bot = telepot.Bot(BOT_TOKEN)


class message():

    def on_callback_query(msg):
        # Get the callback data
        query_id, from_id, query_data = telepot.glance(
            msg, flavor='callback_query')
        # Answer the callback query
        bot.answerCallbackQuery(
            query_id, text='Output size set to {}'.format(query_data))
        # Set the output size
        global OUTPUT_SIZE
        OUTPUT_SIZE = query_data
        log().info('Output size set to {}'.format(query_data))

    def handle_telegram_message(msg):
        content_type, chat_type, chat_id = telepot.glance(msg)

        def set_output_size(bot, chat_id, msg):
            inline_keyboard = [[{'text': f'default({DEFAULT_OUTPUT_SIZE})', 'callback_data': f'{DEFAULT_OUTPUT_SIZE}'}, {
                'text': 'original', 'callback_data': 'original'}]]
            bot.sendMessage(chat_id, 'Select output size:', reply_markup={
                            'inline_keyboard': inline_keyboard})

        def set_discord_channel_id(bot, chat_id, msg):
            if len(msg['text'].split()) != 2:
                bot.sendMessage(
                    chat_id, 'Error: Invalid command. Please send /set DISCORD_CHANNEL_ID')
                return
            global DISCORD_CHANNEL_ID
            DISCORD_CHANNEL_ID = int(msg['text'].split()[1])
            bot.sendMessage(
                chat_id, 'Discord channel ID set to {}'.format(DISCORD_CHANNEL_ID))

        if content_type == 'sticker':
            log().info(
                f"Sticker received from Telegram user: {msg['from']['first_name']}")
            bot.sendChatAction(chat_id, 'upload_photo')
            stickers.stickers.handle_telegram_sticker(
                msg['sticker']['file_id'], chat_id, bot, BOT_TOKEN, DISCORD_TOKEN, DISCORD_CHANNEL_ID, OUTPUT_SIZE)
        elif content_type == 'text':
            bot.sendChatAction(chat_id, 'typing')
            command = msg['text']
            if command.startswith('/'):
                command = command.split()[0]

            # Use a switch-case statement to handle different commands
            case = {
                '/start': lambda: bot.sendMessage(chat_id, 'Hello! I am a sticker bot. Send me a sticker and I will send it to Discord.\n' +
                                                  'send /set to set the Discord channel id to send the sticker to.\n' +
                                                  'send /nowID to get the current Discord channel id.'),
                '/set': lambda: set_discord_channel_id(bot, chat_id, msg),
                '/nowID': lambda: bot.sendMessage(chat_id, 'Current Discord channel ID is {}'.format(DISCORD_CHANNEL_ID)),
                '/size': lambda: set_output_size(bot, chat_id, msg),
            }
            case.get(command, lambda: bot.sendMessage(
                chat_id, 'I only accept stickers.'))()
