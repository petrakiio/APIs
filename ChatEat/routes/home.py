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

home_route = Blueprint('home', __name__)

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




@home_route.route('/remover-carinho/<int:id>')
@login_required
def deletar_item(id):
    sucesso = del_carinho(session['usuario_nome'], id)
    
    if sucesso:
        flash('Item removido!')
        return redirect(url_for('home.carinho'))
    
    flash('Erro ao remover item')
    return redirect(url_for('home.carinho'))