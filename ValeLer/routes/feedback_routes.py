from flask import Blueprint, render_template, redirect, url_for, request, session
from models.feedback import Feedback,FeedbackService
from routes.auth import admin_required

feedback = Blueprint('Feedback', __name__)

@feedback.route('/feedback', methods=['GET', 'POST'])
def feedback_page():
    if request.method == 'POST':
        nome = request.form.get('nome') or session.get('nome')
        gmail = request.form.get('gmail') or session.get('gmail')
        mensagem = request.form.get('mensagem')
        fb = Feedback(nome=nome, gmail=gmail, mensagem=mensagem)
        sucesso, aviso = FeedbackService.enviar_feedback(fb)
        if sucesso:
            return redirect(url_for('Home.index'))
        return render_template('feedback.html', error=aviso)
    return render_template('feedback.html')

@feedback.route('/admin/feedbacks')
@admin_required
def feedback_admin_page():
    return render_template('feedback_admin.html', feedbacks=FeedbackService.listar_feedbacks())

@feedback.route('/del_feed/<int:id>', methods=['POST'])
@admin_required
def del_feed(id):
    if FeedbackService.deletar_feedback(id):
        return redirect(url_for('Feedback.feedback_admin_page'))
    else:
        return "Erro ao deletar o feedback", 400