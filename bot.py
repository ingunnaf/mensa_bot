import os
import telebot
import mensa_scraper as scraper

BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "hello")

@bot.message_handler(commands=['menu', 'food'])
def get_menu(message):
    pdfurl = scraper.getPDFurl()
    bot.send_document(message.chat.id, pdfurl)

@bot.message_handler(commands=['fetch', 'new'])
def download_new_menu(message):
    scraper.downloadMenuPDF()
    bot.reply_to(message, "I downloaded the new menu!")

bot.infinity_polling()
