from flask import Blueprint
from routes.auth import admin_required
from controllers import admin_controller

admin_route = Blueprint('admin', __name__)

@admin_route.route('/admin')
@admin_required
def admin():
    return admin_controller.admin()

@admin_route.route('/admin_user')
@admin_required
def admin_user():
    return admin_controller.admin_user()

@admin_route.route('/admin_produtos')
@admin_required
def admin_produtos():
    return admin_controller.admin_produtos()

@admin_route.route('/admin_produtos/novo', methods=['GET', 'POST'])
@admin_required
def admin_produtos_novo():
    return admin_controller.admin_produtos_novo()

@admin_route.route('/admin_produtos/editar/<int:id>', methods=['GET', 'POST'])
@admin_required
def admin_produtos_editar(id):
    return admin_controller.admin_produtos_editar(id)

@admin_route.route('/admin_produtos/excluir/<int:id>', methods=['GET', 'POST'])
@admin_required
def admin_produtos_excluir(id):
    return admin_controller.admin_produtos_excluir(id)

@admin_route.route('/deletar_feedback/<int:id>')
@admin_required
def deletar_feed(id):
    return admin_controller.deletar_feed(id)

@admin_route.route('/del_user',methods=['POST'])
@admin_required
def deletar_user():
    return admin_controller.deletar_user()

@admin_route.route('/add_admin',methods=['POST'])
@admin_required
def add_admin():
    return admin_controller.add_admin()

@admin_route.route('/rm_admin',methods=['POST'])
@admin_required
def rm_adm():
    return admin_controller.rm_adm()
