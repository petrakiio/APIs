from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from routes.itens import products

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
    
    return render_template('index.html', products=resultados)

@home_route.route('/sobre')
def sobre():
    return render_template('sobre.html')

@home_route.route('/products/<int:id>')
def products_page(id):
    product_found = next((p for p in products if int(p['id']) == id), None)
    
    if product_found:
        return render_template('comprar.html', product=product_found)
    
    return redirect(url_for('home.index'))