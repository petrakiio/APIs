from flask import Blueprint
from controllers import admin_controller

admin = Blueprint('Adm', __name__)


@admin.route('/add_livros_form', methods=['POST'])
def add():
    return admin_controller.add()


@admin.route('/emprestimo_method', methods=['POST'])
def emprestimo_method():
    return admin_controller.emprestimo_method()


@admin.route('/del_book', methods=['POST'])
def del_book():
    return admin_controller.del_book()


@admin.route('/edit_book', methods=['POST'])
def edit_book():
    return admin_controller.edit_book()


@admin.route('/search_books', methods=['GET'])
def search_books():
    return admin_controller.search_books()
