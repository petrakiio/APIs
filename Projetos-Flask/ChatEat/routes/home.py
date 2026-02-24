from flask import Blueprint
from controllers import home_controller

home_route = Blueprint('home', __name__)

@home_route.route('/')
@home_route.route('/index') 
def index():
    return home_controller.index()

@home_route.route('/search', methods=['POST'])
def search():
    return home_controller.search()

@home_route.route('/sobre')
def sobre():
    return home_controller.sobre()

@home_route.route('/status_entrega')
def status_entrega():
    return home_controller.status_entrega()

@home_route.route('/products/<int:id>')
def products_page(id):
    return home_controller.products_page(id)
