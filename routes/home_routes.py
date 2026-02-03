from flask import Blueprint,render_template,redirect,url_for,request
from objects.administração import Livro,BibliotecaService
import os

home = Blueprint('Home',__name__)

@home.route('/')
@home.route('/index')
def index():
    return render_template('index.html',livros=BibliotecaService.home())

@home.route('/add_livros')
def add_livros():
    return render_template('adicionar_livros.html')

@home.route('/add_livros_form',methods=['POST'])
def add():
    livro = Livro(
    titulo=request.form.get('titulo'),
    autor=request.form.get('autor'),
    editora=request.form.get('editora'),
    ano_publicacao=request.form.get('ano_publicacao'),
    isbn=request.form.get('isbn'),
    categoria=request.form.get('categoria'),
    total_unidades=request.form.get('total_unidades'),
    unidades_disponiveis=request.form.get('unidades_disponiveis')
    )
    if BibliotecaService.insert(livro):
        return redirect(url_for('Home.index'))
    else:
        print('erro')
        return redirect(url_for('Home.index'))