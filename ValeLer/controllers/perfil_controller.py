from flask import render_template, redirect, url_for, request, session
from models.perfil import PerfilService


def perfil_page():
    if request.method == "POST":
        img_url = request.form.get("profile_image_url", "").strip()
        if img_url:
            session["img"] = img_url
    return render_template(
        "perfil.html",
        nome=session.get("nome"),
        gmail=session.get("gmail"),
        is_admin=session.get("is_admin", False),
        profile_image_url=session.get("img"),
    )


def devolver_emprestimo():
    nome = request.form.get("nome")
    gmail = request.form.get("gmail")
    usuario = PerfilService.buscar_usuario(nome, gmail)
    if usuario:
        id_emprestimo = PerfilService.get_emprestimo_por_nome(nome)
        if not id_emprestimo:
            return "Empréstimo não encontrado.", 400
        resultado = PerfilService.devolver_emprestimo(id_emprestimo)
        if resultado:
            return redirect(url_for("Home.index"))
        return "Erro ao devolver o livro", 400
    return "Usuário não encontrado.", 400


def atualizar_foto():
    img = request.form.get("profile_image_url", "").strip()
    if img:
        id_usuario = session.get("usuario_id")
        if PerfilService.update_img(id_usuario, img):
            session["img"] = img
            return redirect(url_for("Perfil.perfil_page"))
    return "Erro ao atualizar a foto", 400
