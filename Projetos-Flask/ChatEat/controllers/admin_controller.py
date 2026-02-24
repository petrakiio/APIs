from flask import render_template, url_for, redirect, flash, request
from models.admin_class import AdminService
from models.produtos_class import Product


def _flash_result(result, success_category="success", error_category="danger"):
    if result.get("ok"):
        flash(result.get("msg", "Operação realizada."), success_category)
    else:
        flash(result.get("msg", "Erro ao executar a operação."), error_category)


def admin():
    return render_template("admin.html", feedbacks=AdminService.feedback())


def admin_user():
    return render_template("usuarios.html", cliente=AdminService.users())


def admin_produtos():
    return render_template("admin_produtos.html", produtos=Product.get_all_products())


def admin_produtos_novo():
    if request.method == "POST":
        result = Product.insert_product(
            request.form.get("nome"),
            request.form.get("descricao"),
            float(request.form.get("preco")),
            request.form.get("imagem"),
        )
        _flash_result(result)
        return redirect(url_for("admin.admin_produtos"))
    return render_template("admin_produtos_add.html")


def admin_produtos_editar(id):
    if request.method == "POST":
        result = Product.update_product(
            id,
            request.form.get("nome"),
            request.form.get("descricao"),
            float(request.form.get("preco")),
            request.form.get("imagem"),
        )
        _flash_result(result)
        return redirect(url_for("admin.admin_produtos"))

    produto = Product.get_product_by_id(id)
    if not produto:
        flash("Produto não encontrado.", "danger")
        return redirect(url_for("admin.admin_produtos"))

    produto = {
        "id": produto.get("id"),
        "nome": produto.get("nome", ""),
        "preco": produto.get("preco", ""),
        "descricao": produto.get("descricao", ""),
        "imagem": produto.get("imagem", produto.get("img", "")),
    }
    return render_template("admin_produtos_edit.html", produto=produto)


def admin_produtos_excluir(id):
    result = Product.delete_product(id)
    _flash_result(result)
    return redirect(url_for("admin.admin_produtos"))


def deletar_feed(id):
    result = AdminService.del_fed(id)
    _flash_result(result)
    return redirect(url_for("admin.admin"))


def deletar_user():
    user_id = request.form.get("id")
    result = AdminService.del_user(user_id)
    _flash_result(result)
    return redirect(url_for("admin.admin_user"))


def add_admin():
    user_id = request.form.get("id_admin")
    result = AdminService.add_new_admin(user_id)
    _flash_result(result)
    return redirect(url_for("admin.admin_user"))


def rm_adm():
    user_id = request.form.get("id_admin_remove")
    result = AdminService.rm_admin(user_id)
    _flash_result(result)
    return redirect(url_for("admin.admin_user"))
