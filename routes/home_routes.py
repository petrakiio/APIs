from flask import Blueprint,render_template,redirect,url_for
from objects.administração import BibliotecaService

home = Blueprint('Home',__name__)

@home.route('/')
@home.route('/index')
def index():
    return render_template('index.html',livros=BibliotecaService.home())

@home.route('/add_livros')
def add_livros():
    return render_template('adicionar_livros.html')

@home.route('/add_livros_form')
def add():
    nome =