from flask import Blueprint,render_template,url_for,redirect
from connection.admin_method import feeds,deletar
from auth import admin_required

admin_route = Blueprint('admin', __name__)

admin_route.route('/admin')
def admin():
    return render_template('admin.html',feedbacks=feeds())