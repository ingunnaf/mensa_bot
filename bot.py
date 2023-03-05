import os
import telebot
import mensa_scraper as scraper



BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(commands=['fetch', 'new'])
def fetch_new_menu(message):
    scraper.downloadMenuPDF()
    bot.reply_to(message, "I fetched the new menu for you!")


@bot.message_handler(commands=['menu', 'food'])
def get_menu(message):
    pdfurl = scraper.getPDFurl()
    bot.send_document(message.chat.id, pdfurl)
    #bot.send_document(message, "FILEID")

bot.infinity_polling()


"""f = open("/menu.pdf", 'rb')
    file_bytes = f.read()
    f.close()

    response = {
        'document': (f.name, file_bytes)
    }"""