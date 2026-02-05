from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from models.produtos_class import Product

home_route = Blueprint('home', __name__)

@home_route.route('/')
@home_route.route('/index') 
def index():
    products = Product.get_all_products()
    return render_template('index.html', products=products)

@home_route.route('/search', methods=['POST'])
def search():
    term = request.form.get('search_term', '')
    resultados = Product.search(term)
    return render_template('index.html', products=resultados)

@home_route.route('/sobre')
def sobre():
    return render_template('sobre.html')

@home_route.route('/products/<int:id>')
def products_page(id):
    product_found = Product.get_product_by_id(id)
    
    if product_found:
        return render_template('comprar.html', product=product_found)
    
    return redirect(url_for('home.index'))
