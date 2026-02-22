from flask import flash, render_template, url_for, request, redirect, session
from models.login_class import Pessoa, PersonaService


def login():
    return render_template("login.html")


def recuperar_senha():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")
        confirmar = request.form.get("confirmar_senha")

        if not email or not senha or not confirmar:
            flash("Preencha todos os campos.", "danger")
            return redirect(url_for("Login.recuperar_senha"))

        if senha != confirmar:
            flash("As senhas nao conferem.", "danger")
            return redirect(url_for("Login.recuperar_senha"))

        usuario_id = PersonaService.get_em(email)
        if not usuario_id:
            flash("E-mail nao encontrado.", "danger")
            return redirect(url_for("Login.recuperar_senha"))

        resultado = PersonaService.atualizar_password(senha, usuario_id)
        if not resultado["ok"]:
            flash(resultado["msg"], "danger")
            return redirect(url_for("Login.recuperar_senha"))

        flash(resultado["msg"], "success")
        return redirect(url_for("Login.login"))

    return render_template("recuperar_senha.html")


def cadastro():
    return render_template("cadastro.html")


def inserir():
    pessoa = Pessoa(
        nome=request.form.get("usuario"),
        senha=request.form.get("senha"),
        email=request.form.get("email"),
        data=request.form.get("data"),
    )

    resultado = PersonaService.cadastrar(pessoa)
    if resultado["ok"]:
        flash("Cadastro realizado com sucesso! Faça seu login.", "success")
        return redirect(url_for("Login.login"))

    flash(resultado["msg"], "danger")
    return redirect(url_for("Login.cadastro"))


def busca():
    pessoa = Pessoa(
        nome=request.form.get("usuario"),
        senha=request.form.get("senha"),
        email=None,
        data=None,
    )

    resultado = PersonaService.login(pessoa)
    if not resultado["ok"]:
        flash(resultado["msg"], "danger")
        return redirect(url_for("Login.login"))

    cliente = resultado["cliente"]
    session["usuario_id"] = cliente["id"]
    session["usuario_nome"] = cliente["usuario"]
    session["usuario_image"] = cliente["foto_perfil"]
    session["is_admin"] = bool(cliente["is_admin"])
    session["is_motoboy"] = bool(cliente.get("is_motoboy", False))
    session["is_entregador"] = session["is_motoboy"]
    session.permanent = True

    flash("Login realizado com sucesso!", "success")
    return redirect(url_for("home.index"))


def logout():
    session.pop("usuario_id", None)
    session.pop("usuario_nome", None)
    session.pop("usuario_image", None)
    session.clear()
    return redirect(url_for("home.index"))
