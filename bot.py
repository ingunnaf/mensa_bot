import os
import scraper as scraper
import pytz
from datetime import datetime, time
import logging
import traceback
import html
import json
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

load_dotenv()
CHANNEL_ID = os.environ.get('CHANNEL_ID')
BOT_TOKEN = os.environ.get('BOT_TOKEN')
LOGGER_ID = os.environ.get('LOGGER_ID')

application = Application.builder().token('BOT_TOKEN').build()
job_queue = application.job_queue

tz = pytz.timezone("Europe/Berlin")

# Logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger()


 # Command Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Welcome to the TU Berlin Mensa Menu Update Channel. I will send you the new weekly menu every Monday at 11:30AM. You can also request the menu from me in a private chat at any time by sending me /menu")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="This is the TU Berlin Mensa Telegram Bot. From me you can get the new weekly menu every Monday at 11:30AM. Just join the channel!")

async def send_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    menu = scraper.getPDFurl()
    await context.bot.send_document(chat_id=update.effective_chat.id, document=menu)

async def send_menu_channel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    menu = scraper.getPDFurl()
    await context.bot.send_document(chat_id=CHANNEL_ID, document=menu)

async def send_menu_channel_weekly(context: ContextTypes.DEFAULT_TYPE) -> None:
    menu = scraper.getPDFurl()
    await context.bot.send_document(chat_id=CHANNEL_ID, document=menu)

async def send_menu_channel_weekly_introduction(context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=CHANNEL_ID, text="Here is the menu of the week!")

# Error Handler from the python-telegram-bot examples
# Source: https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/errorhandlerbot.py
async def err_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = ''.join(tb_list)

    # Build the message with some markup and additional information about what happened.
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        f"An exception was raised while handling an update\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
        "</pre>\n\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )
    #await context.bot.send_message(chat_id=LOGGER_CHAT_ID, text=message, parse_mode=telegram.constants.ParseMode.HTML)


def main() -> None:

    app: Application = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("menu", send_menu))
    app.add_handler(CommandHandler("channelmenu", send_menu_channel))

    app.add_error_handler(err_handler)

    app.job_queue.run_daily(send_menu_channel_weekly_introduction, time=time(hour=11, minute=30, tzinfo=tz), days=[1])
    app.job_queue.run_daily(send_menu_channel_weekly, time=time(hour=11, minute=30, tzinfo=tz), days=[1])
    app.run_polling()


if __name__ == "__main__":
    main()
