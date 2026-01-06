import requests
from flask import Blueprint, render_template, request,session, redirect, url_for
from dotenv import load_dotenv
import os
from connection.conn import inserir_cliente, buscar_cliente,criptografar_senha,buscar_senha
from time import time
from routes.auth import login_required
from connection.pedidos import inserir_pedido, gerar_codigo_pedido, consultar_pedido_db
from routes.itens import products


load_dotenv()

def limpar(text):
    return text.replace('@','').replace('<','').replace('>','')


def get_client_ip():
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0]
    return request.remote_addr

def pode_tentar_login(ip):
    dados = login_attempts.get(ip)

    if not dados:
        return True

    tentativas, ultimo_erro = dados

    if tentativas >= MAX_TENTATIVAS:
        if time() - ultimo_erro < BLOQUEIO_TEMPO:
            return False
        else:
            del login_attempts[ip]  # libera depois do tempo

    return True

def registrar_erro_login(ip):
    if ip not in login_attempts:
        login_attempts[ip] = [1, time()]
    else:
        login_attempts[ip][0] += 1
        login_attempts[ip][1] = time()

def resetar_tentativas(ip):
    login_attempts.pop(ip, None)


MAX_TENTATIVAS = 5
BLOQUEIO_TEMPO = 300  
login_attempts = {}
ip_last_order = {}
bot_disc = os.getenv('DISCORD')
home_route = Blueprint('home', __name__)

@home_route.route('/')
@home_route.route('/index') 
def index():
    return render_template('index.html')

@home_route.route('/search', methods=['POST'])
def search():
    iten = request.form.get('search', '')
    for product in products:
        if iten == product['nome']:
            return render_template('index.html', products=[product])
    return '<p>Produto não encontrado.</p><br><a href="/index">Voltar</a>'

@home_route.route('/login')
def login():
    return render_template('login.html')

@home_route.route('/sobre')
def sobre():
    return render_template('sobre.html')

@home_route.route('/pedidos_route')
def pedidos_route():
    return render_template('pedidos.html')

@home_route.route('/consultar-pedido')
def consultar_pedido():
    return render_template('consultar-pedido.html')

@home_route.route('/pedido', methods=['GET', 'POST'])
def pedido():
    if request.method == 'POST':
        ip = get_client_ip()
        agora = time()
        
        #span de tempo entre pedidos
        if ip in ip_last_order and agora - ip_last_order[ip] < 30:
            return '<p>Aguarde 30 segundos antes de enviar outro pedido.</p><br><a href="/pedidos_route">Voltar</a>'

        nome = request.form.get('nome','')
        item = request.form.get('item', '')
        endereco = request.form.get('endereco', '')
        

        if nome == '' or item == '' or endereco == '':
            return '<p>Por favor, preencha todos os campos.</p><br><a href="/pedidos_route">Voltar ao formulário de pedidos</a>'
         #marcando ip
        ip_last_order[ip] = agora

        #tratamento simples
        nome = limpar(nome)
        item = limpar(item)
        endereco = limpar(endereco)
        

        #inserindo pedido no banco
        codigo_pedido = gerar_codigo_pedido()
        sucesso = inserir_pedido(item,codigo_pedido)
        if not sucesso:
            return '<p>Falha ao processar o pedido. Tente novamente mais tarde.</p><br><a href="/pedidos_route">Voltar ao formulário de pedidos</a>'

        payload = {
            "content": f"🔔 **NOVO PEDIDO RECEBIDO**\n"
                       f"👤 **Cliente:** {nome}\n"
                       f"📦 **Item:** {item}\n"
                       f"🏠 **Endereço:** {endereco}\n"
        }   
        try:
            response =requests.post(bot_disc, json=payload)
            if response.status_code == 204:
                return f'<p>Pedido enviado com sucesso!Seu pedido é {codigo_pedido}</p><br><a href="/index">Voltar para a página inicial</a><a href="/consultar-pedido">Como consular pedido?</a>'
            else:
                return f'<p>Falha ao enviar o pedido. Tente novamente mais tarde.</p><br><a href="/pedidos_route">Voltar ao formulário de pedidos</a><p>Seu pedido é {codigo_pedido},Não o perca!</p>'
        except Exception as e:
            return f'<p>Ocorreu um erro: {e}</p>'
    return render_template('pedidos.html')

@home_route.route('/consulta-de-pedido', methods=['POST'])
def consulta_de_pedido():
    codigo = request.form.get('codigo', '')
    if codigo == '':
        return '<p>Por favor, insira o código do pedido.</p><br><a href="/consultar-pedido">Voltar</a>'
    pedido = consultar_pedido_db(codigo)
    if pedido:
        return '<p>Pedido Pronto!</p><br><a href="/index">Voltar</a>'
    return '<p>Ainda em Preparação.</p><br><a href="/index">Voltar</a>'

@home_route.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@home_route.route('/cadastro_cliente', methods=['POST'])
def cadastro_cliente():
    usuario = request.form.get('usuario')
    senha = request.form.get('senha')
    email = request.form.get('email')
    data = request.form.get('data')
    if usuario == '' or senha == '' or email == '' or data == '':
        return '<p>Por favor, preencha todos os campos.</p><br><a href="/cadastro">Voltar ao cadastro</a>'
    if len(usuario) > 50 or len(senha) > 130 or len(email) > 100:
        return redirect(url_for('home.cadastro'))
    senha = criptografar_senha(senha)
    sucesso = inserir_cliente(usuario, senha, email, data)
    if sucesso:
        return '<p>Cadastro realizado com sucesso!</p><br><a href="/login">Ir para o login</a>'
    else:
        return '<p>Falha no cadastro. Tente novamente.</p><br><a href="/cadastro">Voltar ao cadastro</a>'

@home_route.route('/busca', methods=['POST', 'GET'])
def busca():
    if request.method == 'POST':
        ip = get_client_ip()

        if not pode_tentar_login(ip):
            return '<p>Muitas tentativas de login falhadas. Tente novamente mais tarde.</p><br><a href="/login">Voltar ao login</a>'
        

        usuario = request.form.get('usuario')
        senha = request.form.get('senha')
        if len(usuario) > 50 or len(senha) > 100:
            return redirect(url_for('home.login'))
        if usuario == '' or senha == '':
            return '<p>Por favor, preencha todos os campos.</p><br><a href="/login">Voltar ao login</a>'
        else:
            cliente = buscar_cliente(usuario)
            if cliente:
                usuario_id, usuario_nome, senha_hash = cliente
                if buscar_senha(senha, senha_hash):
                    resetar_tentativas(ip)
                    session['usuario_id'] = usuario_id
                    session['usuario_nome'] = usuario_nome
                    session.permanent = True
                    return redirect(url_for('home.index'))
                else:
                    registrar_erro_login(ip)
                    return '<p>Usuário ou senha incorretos.</p><br><a href="/login">Voltar</a>'
            else:
                registrar_erro_login(ip)
                return '<p>Usuário ou senha incorretos.</p><br><a href="/login">Voltar</a>'

    return redirect(url_for('home.login'))

@home_route.route('/logout')
def logout():
    session.pop('usuario_id', None)
    session.pop('usuario_nome', None)
    session.clear()
    return redirect(url_for('home.index'))

@home_route.route('/perfil')
@login_required
def perfil():
    return render_template('perfil.html', usuario_nome=session['usuario_nome'])