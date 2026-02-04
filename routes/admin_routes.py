from flask import Blueprint,request,redirect,url_for
import os
from models.administração import Livro,BibliotecaService
from models.emprestimos import PessoaEmprestimo,EmprestimoService

admin = Blueprint('adm',__name__)

admin.route('/add_livros_form',methods=['POST'])
def add():
    livro = Livro(
        itulo=request.form.get('titulo'),
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

admin.route('/emprestimo_method',methods=['POST'])
def emprestimo_method():
    emprestimo = PessoaEmprestimo(
        id_emprestimo=None,
        id_livro=request.form.get('id_livro'),
        nome_pessoa=request.form.get('nome_pessoa'),
        data_emprestimo=request.form.get('data_emprestimo'),
        data_devolução=request.form.get('data_devolução'),
        valor = request.form.get('valor')
    )
    if EmprestimoService.insert(emprestimo):
        return redirect(url_for('Home.index'))
    else:
        print('erro')