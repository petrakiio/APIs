from flask import Blueprint
from routes.auth import admin_required, login_required
from controllers import home_controller

home = Blueprint('Home', __name__)


@home.route('/')
@home.route('/index')
def index():
    return home_controller.index()


@home.route('/add_livros')
@admin_required
def add_livros():
    return home_controller.add_livros()


@home.route('/emprestimo')
@login_required
def emprestimo():
    return home_controller.emprestimo()


@home.route('/devolver/<int:id>', methods=['POST'])
@admin_required
def devolver(id):
    return home_controller.devolver(id)


@home.route('/deletar')
@admin_required
def deletar():
    return home_controller.deletar()


@home.route('/editar')
@admin_required
def editar():
    return home_controller.editar()


@home.route('/devolver')
def devolver_page():
    return home_controller.devolver_page()
