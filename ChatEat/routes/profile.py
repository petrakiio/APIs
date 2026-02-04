from flask import Blueprint,render_template,redirect,url_for,request,session,flash
import os
from routes.auth import login_required
from models.login_class import PersonaService

profile_route = Blueprint('profile', __name__)

@profile_route.route('/perfil')
@login_required
def perfil():
    if 'usuario_id' not in session:
        return redirect(url_for('home.index'))
        
    return render_template('perfil.html', usuario_nome=session['usuario_nome'])

@profile_route.route('/upload-image', methods=['POST'])
@login_required
def atualizar_imagem():
    img_url = request.form.get('img', '')
    if img_url == '':
        flash('Por favor, insira a URL da imagem.', 'danger')
        return redirect(url_for('profile.perfil'))
    
    sucesso = PersonaService.atulizar(session.get('usuario_id'),img_url)
    if sucesso:
        session['usuario_image'] = img_url
        flash('Imagem de perfil atualizada com sucesso!', 'success')
    else:
        flash('Erro ao atualizar a imagem de perfil.', 'danger')
    return redirect(url_for('profile.perfil'))


@profile_route.route('/deletar/<int:usuario_id>', methods=['POST'])
@login_required
def deletar_conta(usuario_id):
    if 'usuario_id' not in session or session['usuario_id'] != usuario_id:
        return redirect(url_for('home.index'))
    
    sucesso = PersonaService.deletar_method(usuario_id)
    if sucesso:
        session.clear()
        return redirect(url_for('home.index'))
    else:
        return redirect(url_for('profile.perfil'))

