import telebot
from dotenv import load_dotenv
import os
import sys

# Garante que o Python ache a pasta connection
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from connection.pedidos import consultar_pedido_db

load_dotenv()

TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Bem-vindo ao chat da Lucy! Como posso ajudar você hoje?\nUse /pedido [seu_codigo] para consultar.")

@bot.message_handler(commands=['pedido']) # Corrigido para um 'l' só
def consultar_pedido_telegram(message):
    try:
        # Pega o código depois do comando /pedido
        partes = message.text.split()
        if len(partes) < 2:
            return bot.reply_to(message, "Por favor, digite o código. Ex: /pedido 123456")
        
        codigo = partes[1]
        pedido = consultar_pedido_db(codigo) # Abre e fecha a conexão no Filess.io

        if pedido:
            # pedido agora vem como dicionário {'nome': 'valor'} por causa do DictCursor
            bot.reply_to(message, f"Olá {pedido['nome']}, seu pedido foi encontrado e está sendo preparado!")
        else:
            bot.reply_to(message, "Não encontrei nenhum pedido com esse código. Verifique e tente novamente.")
            
    except Exception as e:
        print(f"Erro no bot: {e}")
        bot.reply_to(message, "Houve um erro ao consultar o sistema. Tente novamente mais tarde.")

bot.infinity_polling()