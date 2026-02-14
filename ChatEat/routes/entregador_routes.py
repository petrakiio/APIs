from flask import Blueprint, render_template
from routes.auth import admin_required, entregador_required
from routes.tools import tratamento_dados

entregador_route = Blueprint('entregador', __name__)


@entregador_route.route('/painel_entregador')
@entregador_required
def painel_entregador():
    return render_template('painel_entregador.html')


@entregador_route.route('/admin_entregador')
@admin_required
def admin_entregador():
    return render_template('admin_entregador.html')


@entregador_route.route('/admin_entregador/adicionar',methods=['GET']['POST'])
@admin_required
def admin_add_entregador():
    return render_template('admin_add_entregador.html')


@entregador_route.route('/admin_entregador/visualizar')
@admin_required
def admin_view_entregador():
    return render_template('admin_view_entregador.html')


@entregador_route.route('/admin_entregador/remover')
@admin_required
def admin_remove_entregador():
    return render_template('admin_remove_entregador.html')
