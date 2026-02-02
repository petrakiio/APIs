from flask import Blueprint,render_template,url_for,redirect,flash,request
import os
from class_profile.admin_class import AdminService
from routes.auth import admin_required

admin_route = Blueprint('admin', __name__)

@admin_route.route('/admin')
@admin_required
def admin():
    return render_template('admin.html',feedbacks=AdminService.feedback())

@admin_route.route('/admin_user')
@admin_required
def admin_user():
    return render_template('usuarios.html',cliente=AdminService.users())

@admin_route.route('/deletar_feedback/<int:id>')
@admin_required
def deletar_feed(id):
    r = AdminService.del_fed(id)
    if r['ok']:
        flash(r['msg'],'sucess')
    else:
        flash(r['msg'],'danger')

    return redirect(url_for('admin.admin'))

@admin_route.route('/del_user',methods=['POST'])
@admin_required
def deletar_user():
    id = request.form.get('id')
    r = AdminService.del_user(id)
    if r['ok']:
        flash(r['msg'],'sucess')
    else:
        flash(r['msg'],'danger')
    return redirect(url_for('admin.admin_user'))

@admin_route.route('/add_admin',methods=['POST'])
@admin_required
def add_admin():
    id = request.form.get('id_admin')
    r = AdminService.add_new_admin(id)
    if r['ok']:
        flash(r['msg'],'sucess')
    else:
        flash(r['msg'],'danger')
    return redirect(url_for('admin.admin_user'))

@admin_route.route('/rm_admin',methods=['POST'])
@admin_required
def rm_adm():
    id = request.form.get('id_admin_remove')
    r = AdminService.rm_admin(id)
    if r['ok']:
        flash(r['msg'],'sucess')
    else:
        flash(r['msg'],'danger')
    return redirect(url_for('admin.admin_user'))