from flask import blueprints,render_template

home_route = blueprints.Blueprint('home', __name__)

@home_route.route('/')
def home():
    return render_template('index.html')

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

@home_route.route('/pedido')
def pedido():
    pass  # Lógica para processar o pedido