from flask import Blueprint, render_template, redirect, url_for, request, session
import os
from models.perfil import PerfilService
from routes.auth import login_required

perfil = Blueprint('Perfil', __name__)

@perfil.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil_page():
    if request.method == 'POST':
        img_url = request.form.get('profile_image_url', '').strip()
        if img_url:
            session['img'] = img_url
    return render_template(
        'perfil.html',
        nome=session.get('nome'),
        gmail=session.get('gmail'),
        is_admin=session.get('is_admin', False),
        profile_image_url=session.get('img')
    )

@perfil.route('/devolver_emprestimo', methods=['POST'])
@login_required
def devolver_emprestimo():
    nome = request.form.get('nome')
    gmail = request.form.get('gmail')
    usuario = PerfilService.buscar_usuario(nome, gmail)
    if usuario:
        id_emprestimo = PerfilService.get_emprestimo_por_nome(nome)
        if not id_emprestimo:
            return "Empréstimo não encontrado.", 400
        resultado = PerfilService.devolver_emprestimo(id_emprestimo)
        if resultado:
            return redirect(url_for('Home.index'))
        else:
            return "Erro ao devolver o livro", 400
@perfil.route('/atualizar_foto', methods=['POST'])
@login_required
def atualizar_foto():
    img = request.form.get('profile_image_url', '').strip()
    if img:
        id_usuario = session.get('usuario_id')
        if PerfilService.update_img(id_usuario, img):
            session['img'] = img
            return redirect(url_for('Perfil.perfil_page'))
    return "Erro ao atualizar a foto", 400
