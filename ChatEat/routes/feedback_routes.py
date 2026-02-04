from flask import Blueprint, render_template, request, session, redirect, url_for,flash
from routes.auth import login_required
from models.feedback_class import FeedbackService

feedback_route = Blueprint('feed',__name__)

@feedback_route.route('/feedback')
@login_required
def feedback():
    return render_template('feedback.html')

@feedback_route.route('/enviar-feed', methods=['POST'])
@login_required
def enviar():
    user = session.get('usuario_id')
    comentario = request.form.get('comentario', '')
    nota = request.form.get('nota', '')
    r = FeedbackService.enviar(user,comentario,nota)
    if r['ok']:
        flash(r['msg'],'success')
    else:
        flash(r['msg'],'danger')
    return redirect(url_for('home.index'))
