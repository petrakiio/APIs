import requests
from flask import Blueprint, render_template, request, session, redirect, url_for,flash
from dotenv import load_dotenv
import os
from connection.conn import inserir_cliente, buscar_cliente, criptografar_senha, buscar_senha,get_itens_carrinho,atualizar_imagem_perfil, verificar_email,deletar,add_carinho,del_carinho,add_com
from time import time
from routes.auth import login_required
from routes.itens import products
from datetime import datetime


load_dotenv()

# ==========================================
# CONFIGURAÇÕES E UTILITÁRIOS
# ==========================================

MAX_TENTATIVAS = 5
BLOQUEIO_TEMPO = 300  
login_attempts = {}
ip_last_order = {}
home_route = Blueprint('home', __name__)


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



@home_route.route('/logout')
def logout():
    session.pop('usuario_id', None)
    session.pop('usuario_nome', None)
    session.clear()
    return redirect(url_for('home.index'))

@home_route.route('/deletar/<int:id>/<string:user>', methods=['POST'])
@login_required
def delete(id, user):
    if not user:
        return 'Erro'
    
    if session['usuario_id'] != id:
        return "Acesso negado", 403

 
    if deletar(int(id), str(user)):
        session.clear()
        flash("Sua conta foi excluída com sucesso. Sentiremos sua falta!", "success")
        return redirect(url_for('home.index'))
    
    flash("Não foi possível excluir sua conta. Tente novamente mais tarde.", "danger")
    return "Erro ao deletar", 500


# ==========================================
# ROTAS DE PERFIL DO USUÁRIO
# ==========================================

@home_route.route('/perfil')
@login_required
def perfil():
    
    if 'usuario_id' not in session:
        return redirect(url_for('home.index'))
        
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

@home_route.route('/feedback')
@login_required
def feed():
    return render_template('feedback.html')


@home_route.route('/enviar-feed', methods=['POST'])
@login_required
def enviar_comentario():
    user = session.get('usuario_id')
    comentario = request.form.get('comentario', '')
    nota = request.form.get('nota', '')
    
    if not comentario or not nota:
        flash('Por favor, preencha todos os campos.', 'warning')
        return redirect(url_for('home.feed'))
    
    r = add_com(user, comentario, nota)
    
    if r:
        flash('Comentário enviado com sucesso!', 'success')
    else:
        flash('Erro ao enviar comentário.', 'danger')
        
    return redirect(url_for('home.feed'))

# ==========================================
# ROTAS DE PEDIDOS E VENDAS
# ==========================================

@home_route.route('/products/<int:id>')
def products_page(id):
    for produto in products:
        if produto['id'] == id:
            return render_template('comprar.html',product=produto)
    else:
        pass

@home_route.route('/adicionar-carinho/<int:id>')
@login_required
def adicionar(id):
    for produto in products:
        if produto['id'] == id:
            add_carinho(session['usuario_nome'], produto['id'])
            flash('Item adicionado ao carrinho')
            return redirect(url_for('home.carinho'))

    return redirect(url_for('home.index'))


@home_route.route('/carinho')
@login_required
def carinho():
    ids_no_banco = get_itens_carrinho(session['usuario_nome'])

    carrinho_completo = []
    for p_id in ids_no_banco:
        for p in products:
            if p['id'] == p_id:
                carrinho_completo.append(p)
                break
    
    return render_template('carinho.html', carrinho=carrinho_completo)

@home_route.route('/remover-carinho/<int:id>')
@login_required
def deletar_item(id):
    sucesso = del_carinho(session['usuario_nome'], id)
    
    if sucesso:
        flash('Item removido!')
        return redirect(url_for('home.carinho'))
    
    flash('Erro ao remover item')
    return redirect(url_for('home.carinho'))