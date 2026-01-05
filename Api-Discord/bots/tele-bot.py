#bot pra usuarios interagirem via telegram

import telebot
from dotenv import load_dotenv
import os
from connection.pedidos import consultar_pedido_db

load_dotenv()

TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Bem-vindo ao chat da Lucy! Como posso ajudar você hoje?")

@bot.message_handller(commands=['pedido'])
def fazer_pedido(message):
        bot.reply_to(message, "Me diga o seu codigo para consultar o pedido.")
        codigo = message.text.split()[1]
        pedido = consultar_pedido_db(codigo)
        if pedido:
            bot.reply_to(message, "Seu pedido está sendo preparado!")
        else:
             bot.reply_to(message, "Seu pedido está em preparação!")

bot.infinity_polling()