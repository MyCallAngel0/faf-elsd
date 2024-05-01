from typing import Final
from telegram import Update, ForceReply
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext
import json
from chatbot import ask_prompt

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
    await update.message.reply_text("Sure! How can i help?")


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! What can I do for you?")


async def itt_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Please send an image.", reply_markup=ForceReply(selective=True))


async def ask_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please insert the prompt", reply_markup=ForceReply(selective=True))


# Responses
async def handle_response(update: Update, text: str) -> str:
    processed = text.lower()
    return str(await ask_prompt(text))
    if 'hello' in processed:
        return 'Hey there!'
    if 'whisper' in processed:
        return 'Send audio file'
    if 'ask' in processed:
        return 'This is your answer'

    return 'I don\'t understand.'


async def handle_image(update: Update, context: CallbackContext):
    photo = update.message.photo[-1]
    photo_file = await context.bot.get_file(photo.file_id)  # Retrieve the file from Telegram servers using the file ID
    await photo_file.download('received_image.jpg')  # Download the image and save it locally
    await update.message.reply_text('Image saved! Now processing...')
    # Here you can add the function that will use the saved image
    process_image('received_image.jpg')


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


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} cause error {context.error}')


def process_image(image_path):
    # Your image processing function here
    print(f"Processing image: {image_path}")


if __name__ == "__main__":
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('itt', itt_command))
    app.add_handler(CommandHandler('ask', ask_command))

    # Messages
    app.add_handler((MessageHandler(filters.TEXT, handle_message)))
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    app.run_polling(poll_interval=3)

