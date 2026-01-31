from flask import Blueprint, render_template, request, session, redirect, url_for,flash
from routes.itens import products


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