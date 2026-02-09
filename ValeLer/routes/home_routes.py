from flask import Blueprint,render_template,redirect,url_for,request,session
from models.administração import BibliotecaService
from models.emprestimos import EmprestimoService
from routes.auth import admin_required,login_required

home = Blueprint('Home',__name__)

@home.route('/')
@home.route('/index')
def index():
    return render_template(
        'index.html',
        livros=BibliotecaService.home(),
        emprestimos=EmprestimoService.home(),
        livros_user=EmprestimoService.user_livros(session.get('nome')) if 'usuario_id' in session else []
    )

@home.route('/add_livros')
@admin_required
def add_livros():
    return render_template('adicionar_livros.html')


@home.route('/emprestimo')
@login_required
def emprestimo():
    return render_template('emprestar_livros.html',livros=BibliotecaService.home())

@home.route('/devolver/<int:id>', methods=['POST'])
@admin_required
def devolver(id):
        r = EmprestimoService.delete(id)
        if r:
            return redirect(url_for('Home.index'))
        else:
            return "Erro ao devolver o livro", 400
@home.route('/deletar')
@admin_required
def deletar():
    return render_template('deletar.html')

@home.route('/editar')
@admin_required
def editar():
    return render_template('editar_livros.html')

@home.route('/devolver')
def devolver_page():
    return render_template('devolver.html')
