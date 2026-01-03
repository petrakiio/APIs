import requests
from flask import Blueprint, render_template, request 
from dotenv import load_dotenv
import os

load_dotenv()

bot_disc = os.getenv('DISCORD')
home_route = Blueprint('home', __name__)

@home_route.route('/')
@home_route.route('/index') 
def index():
    return render_template('index.html')

@home_route.route('/login')
def login():
    return render_template('login.html')

@home_route.route('/sobre')
def sobre():
    return render_template('sobre.html')

@home_route.route('/pedidos_route')
def pedidos_route():
    return render_template('pedidos.html')

@home_route.route('/pedido', methods=['GET', 'POST'])
def pedido():
    if request.method == 'POST':
        nome = request.form.get('nome')
        item = request.form.get('item')
        endereco = request.form.get('endereco')
        payload = {
            "content": f"🔔 **NOVO PEDIDO RECEBIDO**\n"
                       f"👤 **Cliente:** {nome}\n"
                       f"📦 **Item:** {item}\n"
                       f"🏠 **Endereço:** {endereco}"
        }   
        try:
            response =requests.post(bot_disc, json=payload)
            if response.status_code == 204:
                return '<p>Pedido enviado com sucesso!</p>'
            else:
                return '<p>Falha ao enviar o pedido. Tente novamente mais tarde.</p>'
        except Exception as e:
            return f'<p>Ocorreu um erro: {e}</p>'
    return render_template('pedidos.html')