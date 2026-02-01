from flask import Blueprint,render_template,url_for,redirect,flash
from class_profile import admin_class
from routes.auth import admin_required

admin_route = Blueprint('admin', __name__)

@admin_route.route('/admin')
@admin_required
def admin():
    return render_template('admin.html',feedbacks=feeds())

@admin_route.route('/admin_user')
@admin_required
def admin_user():
    pass

@admin_route.route('/deletar_feedback/<int:id>')
@admin_required
def deletar_feed(id):
    if deletar(id):
        flash('Item removido!')
    else:
        flash('Erro ao remover')
        
    return redirect(url_for('admin.admin'))