import requests
from flask import Blueprint, render_template, request, session, redirect, url_for,flash
from dotenv import load_dotenv
import os
from connection.conn import inserir_cliente, buscar_cliente, criptografar_senha, buscar_senha, atualizar_imagem_perfil, verificar_email,deletar
from time import time
from routes.auth import login_required
from connection.pedidos import inserir_pedido, gerar_codigo_pedido, consultar_pedido_db
from routes.itens import products
from routes.validação import enviar_codigo,criar_codigo
from datetime import datetime

load_dotenv()

# ==========================================
# CONFIGURAÇÕES E UTILITÁRIOS
# ==========================================

MAX_TENTATIVAS = 5
BLOQUEIO_TEMPO = 300  
login_attempts = {}
ip_last_order = {}
bot_disc = os.getenv('DISCORD')
home_route = Blueprint('home', __name__)

def limpar(text):
    return text.replace('@','').replace('<','').replace('>','')

def get_client_ip():
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0]
    return request.remote_addr

# ==========================================
# Validação de idade
# ==========================================

def validar_idade(data_nascimento_str, idade_minima):
    try:
        data_nasc = datetime.strptime(data_nascimento_str, '%Y-%m-%d')
        hoje = datetime.today()
        idade = hoje.year - data_nasc.year - ((hoje.month, hoje.day) < (data_nasc.month, data_nasc.day))
        return idade >= idade_minima
    except Exception as e:
        print(f"Erro na data: {e}")
        return False

# ==========================================
# SEGURANÇA E TENTATIVAS DE LOGIN
# ==========================================

def pode_tentar_login(ip):
    dados = login_attempts.get(ip)
    if not dados:
        return True
    tentativas, ultimo_erro = dados
    if tentativas >= MAX_TENTATIVAS:
        if time() - ultimo_erro < BLOQUEIO_TEMPO:
            return False
        else:
            del login_attempts[ip]
    return True

def registrar_erro_login(ip):
    if ip not in login_attempts:
        login_attempts[ip] = [1, time()]
    else:
        login_attempts[ip][0] += 1
        login_attempts[ip][1] = time()

def resetar_tentativas(ip):
    login_attempts.pop(ip, None)

# ==========================================
# ROTAS DE NAVEGAÇÃO E BUSCA
# ==========================================

@home_route.route('/')
@home_route.route('/index') 
def index():
    return render_template('index.html', products=products)

@home_route.route('/search', methods=['POST'])
def search():
    iten = request.form.get('search', '').lower().strip()
    if not iten:
        return render_template('index.html', products=products)
    resultados = [
        p for p in products
        if iten in p['nome'].lower() or iten in p['descricao'].lower()
    ]
    if resultados:
        return render_template('index.html', products=resultados)
    return render_template('index.html', products=[], mensagem="Nenhum prato encontrado com esse nome.")

@home_route.route('/sobre')
def sobre():
    return render_template('sobre.html')

# ==========================================
# ROTAS DE AUTENTICAÇÃO (LOGIN E CADASTRO)
# ==========================================

@home_route.route('/login')
def login():
    return render_template('login.html')

@home_route.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@home_route.route('/cadastro_cliente', methods=['POST'])
def cadastro_cliente():
    usuario = request.form.get('usuario')
    senha = request.form.get('senha')
    email = request.form.get('email')
    data = request.form.get('data')

    #Validação de idade
    if not validar_idade(data,18):
        flash('Você é novo demais!','danger')
        return render_template('cadastro.html')

    #Verificação de email cadastro
    resultado = verificar_email(email)
    if resultado:
        flash('Seu email já esta logado!','danger')
        return render_template('cadastro.html')

    # Validações básicas
    if not all([usuario, senha, email, data]):
        flash('Por favor, preencha todos os campos.', 'danger')
        return redirect(url_for('home.cadastro'))

    #Gera o código e enviar
    codigo_gerado = criar_codigo()
    print(codigo_gerado)
    sucesso_email = enviar_codigo(codigo_gerado, email)

    if sucesso_email:
        session['temp_usuario'] = usuario
        session['temp_senha'] = criptografar_senha(senha)
        session['temp_email'] = email
        session['temp_data'] = data
        session['codigo_validacao'] = codigo_gerado

        flash('Enviamos uma validação de email!', 'info')
        return render_template('verificar.html') 
    else:
        flash('Erro ao enviar e-mail de validação. Tente novamente.', 'danger')
        return redirect(url_for('home.cadastro'))

@home_route.route('/confirmar_email',methods=['POST'])
def confirmar():
    codigo_real = session['codigo_validacao']
    codigo_dig = request.form.get('codigo')
    if codigo_dig == codigo_real:
        sucesso = inserir_cliente(
            session['temp_usuario'],
            session['temp_senha'],
            session['temp_email'],
            session['temp_data']
        )
        if sucesso:
            session.clear()
            flash('Usuario criado com sucesso!')
            return redirect(url_for('home.index'))
        else:
            flash('Erro')
            return redirect(url_for('home.cadastro'))
    else:
        flash('Codigo Errado!')
        return render_template('verificar.html')

@home_route.route('/busca', methods=['POST', 'GET'])
def busca():
    if request.method == 'POST':
        ip = get_client_ip()
        if not pode_tentar_login(ip):
            flash('Muitas tentativas, tente depois')
            return redirect(url_for('home.index'))
        
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')
        if len(usuario) > 50 or len(senha) > 100:
            return redirect(url_for('home.login'))
        if usuario == '' or senha == '':
            flash('Dados faltando!')
            return redirect(url_for('home.login'))
        
        cliente = buscar_cliente(usuario)
        if cliente:
            usuario_id = cliente['id']
            usuario_nome = cliente['usuario']
            senha_hash = cliente['senha']
            img = cliente['foto_perfil']
            if buscar_senha(senha, senha_hash):
                resetar_tentativas(ip)
                session['usuario_id'] = usuario_id
                session['usuario_nome'] = usuario_nome
                session['usuario_image'] = img
                session.permanent = True
                flash('Login realizado com sucesso!')
                return redirect(url_for('home.index'))
            else:
                registrar_erro_login(ip)
                flash('Usario ou senha incorretos')
                return redirect(url_for('home.login'))
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

@home_route.route('/deletar', methods=['POST'])
def delete():
    id = session.get('usuario_id')
    user = session.get('usuario_nome')

    if not id or not user:
        return '', 401

    resultado = deletar(id,user)

    if resultado:
        session.pop('usuario_id', None)
        session.pop('usuario_nome', None)
        return '', 204

    return '', 400



# ==========================================
# ROTAS DE PERFIL DO USUÁRIO
# ==========================================

@home_route.route('/perfil')
@login_required
def perfil():
    
    if 'usuario_id' not in session:
        redirect(url_for('home.index'))
        
    return render_template('perfil.html', usuario_nome=session['usuario_nome'])

@home_route.route('/upload-image', methods=['POST'])
@login_required
def upload_image():
    img_url = request.form.get('img', '')
    if img_url == '':
        return '<p>Por favor, insira a URL da imagem.</p><br><a href="/perfil">Voltar</a>'
    
    atualizar_imagem_perfil(session['usuario_id'], img_url)
    session['usuario_image'] = img_url
    return redirect(url_for('home.perfil'))

# ==========================================
# ROTAS DE PEDIDOS E VENDAS
# ==========================================

@home_route.route('/consultar-pedido')
def consultar_pedido():
    return render_template('consultar_pedido.html')

@home_route.route('/consulta-de-pedido', methods=['POST'])
def consulta_de_pedido():
    codigo = request.form.get('codigo', '')
    if not codigo:
        return '<p>Por favor, insira o código do pedido.</p><br><a href="/consultar-pedido">Voltar</a>'
    
    pedido = consultar_pedido_db(codigo)
    if pedido:
        return '<p>Pedido Pronto!</p><br><a href="/index">Voltar</a>'
    return '<p>Ainda em Preparação.</p><br><a href="/index">Voltar</a>'

@home_route.route('/products/<int:id>')
def products_page(id):
    for produto in products:
        if produto['id'] == id:
            return render_template('comprar.html',product=produto)
    else:
        pass
