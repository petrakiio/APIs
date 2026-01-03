import requests
from flask import Blueprint, render_template, request,session, redirect, url_for
from dotenv import load_dotenv
import os
from conn import inserir_cliente, buscar_cliente,criptografar_senha,buscar_senha

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
                return '<p>Pedido enviado com sucesso!</p><br><a href="/index">Voltar para a página inicial</a>'
            else:
                return '<p>Falha ao enviar o pedido. Tente novamente mais tarde.</p><br><a href="/pedidos_route">Voltar ao formulário de pedidos</a>'
        except Exception as e:
            return f'<p>Ocorreu um erro: {e}</p>'
    return render_template('pedidos.html')

@home_route.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@home_route.route('/cadastro_cliente', methods=['POST'])
def cadastro_cliente():
    usuario = request.form.get('usuario')
    senha = request.form.get('senha')
    email = request.form.get('email')
    data = request.form.get('data')
    senha = criptografar_senha(senha)
    sucesso = inserir_cliente(usuario, senha, email, data)
    if sucesso:
        return '<p>Cadastro realizado com sucesso!</p><br><a href="/login">Ir para o login</a>'
    else:
        return '<p>Falha no cadastro. Tente novamente.</p><br><a href="/cadastro">Voltar ao cadastro</a>'

@home_route.route('/busca', methods=['POST', 'GET'])
def busca():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')
        cliente = buscar_cliente(usuario)
        if cliente and buscar_senha(senha, cliente[2]):
            session['usuario_id'] = cliente[0]
            session['usuario_nome'] = cliente[1]
            return f'<p>Login bem-sucedido! Bem-vindo, {cliente[1]}.</p><br><a href="/perfil">Ir para o perfil</a>'
    return '<p>Falha no login. Usuário ou senha incorretos.</p><br><a href="/login">Voltar ao login</a>'

@home_route.route('/logout')
def logout():
    session.pop('usuario_id', None)
    session.pop('usuario_nome', None)
    return redirect(url_for('home.index'))

@home_route.route('/perfil')
def perfil():
    if 'usuario_id' not in session:
        return redirect(url_for('home.login')) and '<p>Você precisa estar logado para acessar o perfil.</p><br><a href="/login">Ir para o login</a>'
    return render_template('perfil.html', usuario_nome=session['usuario_nome'])