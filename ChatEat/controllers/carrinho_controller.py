from flask import session, redirect, render_template, url_for, flash
from models.carrinho_class import CarrinhoService


def carrinho():
    resultado = CarrinhoService.listar(session.get("usuario_nome"))
    if not resultado["ok"]:
        flash(resultado["msg"], "danger")
        return redirect(url_for("home.index"))

    return render_template("carinho.html", carrinho=resultado["carrinho"])


def adicionar(id):
    result = CarrinhoService.add(id, session.get("usuario_nome"))
    if result["ok"]:
        flash(result["msg"], "success")
    elif result["ok"] is None:
        flash(result["msg"], "danger")
    else:
        flash(result["msg"], "danger")
    return redirect(url_for("home.index"))


def deletar_item(id):
    result = CarrinhoService.dell(session.get("usuario_nome"), id)
    if result["ok"]:
        flash(result["msg"], "success")
    else:
        flash(result["msg"], "danger")
    return redirect(url_for("carrinho.carrinho"))


def confirmar_compra():
    flash("Checkout ainda não implementado.", "danger")
    return redirect(url_for("home.index"))
