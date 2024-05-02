from typing import Final
from telegram import Update, ForceReply
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext
import json
from chatbot import ask_prompt
from imageToText import image_to_text

with open('tokens.json', 'r') as file:
    data = json.load(file)

TOKEN: Final = data['TELEGRAM_BOT']
BOT_USERNAME: Final = '@SOLeAI_bot'

states = {}
ask: bool = False


# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! What can I do for you?")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
/start - Starts the bot
/help - Provides this message
/convert - Converts image or audio file to text
""")


async def convert_command(update: Update, context: CallbackContext):
    states[update.message.chat_id] = 'awaiting_file'
    await update.message.reply_text("Please send an image or audio.", reply_markup=ForceReply(selective=True))


# Responses
async def handle_response(update: Update, text: str) -> str:
    return str(await ask_prompt(update.message.chat_id, text))


async def handle_image(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    if chat_id not in states or states[chat_id] != 'awaiting_file':
        return  # Ignore images if not requested
    photo = update.message.photo[-1]
    photo_file = await context.bot.get_file(photo.file_id)  # Retrieve the file from Telegram servers using the file ID
    file_bytes = await photo_file.download_as_bytearray()
    file_path = "received_image.jpg"
    with open(file_path, "wb") as file:
        file.write(file_bytes)
    await update.message.reply_text(image_to_text(file_path))
    del states[chat_id]


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = await handle_response(new_text)
        else:
            return
    else:
        response: str = await handle_response(update, text)

    print('Bot:', response)
    await update.message.reply_text(response)


async def handle_audio(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    if chat_id not in states or states[chat_id] != 'awaiting_file':
        return  # Ignore images if not requested
    # audio = update.message.audio[-1]
    # audio_file = await context.bot.get_file(audio.file_id)  # Retrieve the file from Telegram servers using the file ID
    # file_bytes = await audio_file.download_as_bytearray()
    # file_path = "received_image.jpg"
    # with open(file_path, "wb") as file:
    #     file.write(file_bytes)
    del states[chat_id]
    response = "Converting audio to text is currently not working. Sorry for the inconvenience."
    print('Bot:', response)
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} cause error {context.error}')


if __name__ == "__main__":
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('convert', convert_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))
    app.add_handler(MessageHandler(filters.AUDIO, handle_audio))
    app.add_handler(MessageHandler(filters.VOICE, handle_audio))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    app.run_polling(poll_interval=3)

