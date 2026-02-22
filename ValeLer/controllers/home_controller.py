from flask import render_template, redirect, url_for, session
from models.administração import BibliotecaService
from models.emprestimos import EmprestimoService


def index():
    return render_template(
        "index.html",
        livros=BibliotecaService.home(),
        emprestimos=EmprestimoService.home(),
        livros_user=EmprestimoService.user_livros(session.get("nome"))
        if "usuario_id" in session
        else [],
    )


def add_livros():
    return render_template("adicionar_livros.html")


def emprestimo():
    return render_template("emprestar_livros.html", livros=BibliotecaService.home())


def devolver(id):
    result = EmprestimoService.delete(id)
    if result:
        return redirect(url_for("Home.index"))
    return "Erro ao devolver o livro", 400


def deletar():
    return render_template("deletar.html")


def editar():
    return render_template("editar_livros.html")


def devolver_page():
    return render_template("devolver.html")
