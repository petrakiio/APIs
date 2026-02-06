from flask import Blueprint,render_template,redirect,url_for,request
from models.administração import BibliotecaService
from models.emprestimos import EmprestimoService

home = Blueprint('Home',__name__)

@home.route('/')
@home.route('/index')
def index():
    return render_template('index.html',livros=BibliotecaService.home(),emprestimos=EmprestimoService.home())

@home.route('/add_livros')
def add_livros():
    return render_template('adicionar_livros.html')


@home.route('/emprestimo')
def emprestimo():
    return render_template('emprestar_livros.html',livros=BibliotecaService.home())

@home.route('/devolver/<int:id>', methods=['POST'])
def devolver(id):
        r = EmprestimoService.delete(id)
        if r:
            return redirect(url_for('Home.index'))
        else:
            return "Erro ao devolver o livro", 400
@home.route('/deletar')
def deletar():
    return render_template('deletar.html')

@home.route('/editar')
def editar():
    return render_template('editar_livros.html')
