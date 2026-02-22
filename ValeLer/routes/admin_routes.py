from flask import Blueprint, request, redirect, url_for, jsonify,session
from models.administração import Livro, BibliotecaService
from models.emprestimos import PessoaEmprestimo, EmprestimoService
from routes.auth import admin_required, login_required

admin = Blueprint('Adm', __name__)

@admin.route('/add_livros_form', methods=['POST'])
@admin_required
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
    BibliotecaService.insert(livro)
    return redirect(url_for('Home.index'))


@admin.route('/emprestimo_method', methods=['POST'])
@login_required
def emprestimo_method():
    emprestimo = PessoaEmprestimo(
        id_emprestimo=None,
        id_livro=request.form.get('id_livro'),
        nome_pessoa=request.form.get('nome_pessoa') or session.get('nome'),
        data_emprestimo=request.form.get('data_emprestimo'),
        data_devolucao=request.form.get('data_devolucao'),
        valor=request.form.get('valor') or '10,00'
    )
    EmprestimoService.insert(emprestimo)
    print('funcionou')
    return redirect(url_for('Home.index'))

@admin.route('/del_book', methods=['POST'])
@admin_required
def del_book():
    id_livro = request.form.get('id_livro')
    if EmprestimoService.delete_livro(id_livro):
        return redirect(url_for('Home.index'))
    else:
        return "Erro ao deletar o livro", 400

@admin.route('/edit_book', methods=['POST'])
@admin_required
def edit_book():
    id = request.form.get('id_livro')
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
    if BibliotecaService.edit_book(id, livro):
        return redirect(url_for('Home.index'))
    else:
        return "Erro ao editar o livro", 400

@admin.route('/search_books', methods=['GET'])
@admin_required
def search_books():
    query = request.args.get('q')
    results = BibliotecaService.search_books(query)
    return jsonify(results)
