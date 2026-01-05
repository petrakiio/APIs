import telebot
from dotenv import load_dotenv
import os
load_dotenv()

TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Bem-vindo ao chat da Lucy! Como posso ajudar você hoje?")

@bot.message_handller(commands=['pedido'])



bot.infinity_polling()