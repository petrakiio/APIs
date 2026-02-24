from flask import render_template, request, flash, url_for, redirect
from routes.tools import tratamento_dados
from models.entregador_class import Entregador, EntregadoService
from models.registro_class import Registro, RegistroService


def painel_entregador():
    return render_template("painel_entregador.html")


def admin_entregador():
    return render_template("admin_entregador.html")


def admin_add_entregador():
    if request.method == "POST":
        entregador = Entregador(
            nome=tratamento_dados(request.form.get("nome")),
            usuario=request.form.get("usuario"),
            email=request.form.get("email"),
            telefone=request.form.get("telefone"),
            veiculo=request.form.get("veiculo"),
            placa=request.form.get("placa"),
            ativo=True,
        )
        if not entregador.nome:
            flash("Complete os Dados")
            return redirect(url_for("entregador.admin_add_entregador"))

        result = EntregadoService.add(entregador)
        if result:
            flash("Entregador adicionado com sucesso!")
            return redirect(url_for("entregador.admin_view_entregador"))
        flash("Erro ao adicionar entregado:(")
        return redirect(url_for("entregador.painel_entregador"))

    return render_template("admin_add_entregador.html")


def admin_view_entregador():
    return render_template(
        "admin_view_entregador.html",
        entregadores=EntregadoService.visu(),
    )


def admin_remove_entregador():
    if request.method == "POST":
        registro = Registro(
            nome=tratamento_dados(request.form.get("nome")),
            mt=request.form.get("motivo"),
            obs=request.form.get("observacao"),
        )

        if not RegistroService.add_m(registro):
            flash("Erro ao registrar motivo da remocao!")
            return redirect(url_for("entregador.admin_remove_entregador"))

        if EntregadoService.rm(registro.nome):
            flash("Entregador removido com sucesso!")
            return redirect(url_for("entregador.admin_view_entregador"))

        flash("Erro ao deletar!")
        return redirect(url_for("entregador.admin_remove_entregador"))

    return render_template(
        "admin_remove_entregador.html",
        entregadores=EntregadoService.visu(),
    )
