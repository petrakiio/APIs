from flask import Blueprint, render_template, request, flash, url_for, redirect
from routes.auth import admin_required, entregador_required
from routes.tools import tratamento_dados
from models.entregador_class import Entregador, EntregadoService
from models.registro_class import Registro, RegistroService

entregador_route = Blueprint('entregador', __name__)


@entregador_route.route('/painel_entregador')
@entregador_required
def painel_entregador():
    return render_template('painel_entregador.html')


@entregador_route.route('/admin_entregador')
@admin_required
def admin_entregador():
    return render_template('admin_entregador.html')


@entregador_route.route('/admin_entregador/adicionar',methods=['GET', 'POST'])
@admin_required
def admin_add_entregador():
    if request.method == 'POST':
        nome = request.form.get('nome')
        entregador = Entregador(
        nome=tratamento_dados(nome),
        usuario=request.form.get('usuario'),
        email=request.form.get('email'),
        telefone=request.form.get('telefone'),
        veiculo=request.form.get('veiculo'),
        placa=request.form.get('placa'),
        ativo=True
        )
        if not entregador.nome:
            flash('Complete os Dados')
            return redirect(url_for('entregador.admin_add_entregador'))

        r = EntregadoService.add(entregador)
        if r:
            flash('Entregador adicionado com sucesso!')
            return redirect(url_for('entregador.admin_view_entregador'))
        flash('Erro ao adicionar entregado:(')
        return redirect(url_for('entregador.painel_entregador'))


    return render_template('admin_add_entregador.html')


@entregador_route.route('/admin_entregador/visualizar')
@admin_required
def admin_view_entregador():
    return render_template('admin_view_entregador.html', entregadores=EntregadoService.visu())


@entregador_route.route('/admin_entregador/remover',methods=['POST', 'GET'])
@admin_required
def admin_remove_entregador():
    if request.method == 'POST':
        registro = Registro(
            nome=tratamento_dados(request.form.get('nome')),
            mt=request.form.get('motivo'),
            obs=request.form.get('observacao'),
        )

        if not RegistroService.add_m(registro):
            flash('Erro ao registrar motivo da remocao!')
            return redirect(url_for('entregador.admin_remove_entregador'))

        if EntregadoService.rm(registro.nome):
            flash('Entregador removido com sucesso!')
            return redirect(url_for('entregador.admin_view_entregador'))

        flash('Erro ao deletar!')
        return redirect(url_for('entregador.admin_remove_entregador'))

    return render_template(
        'admin_remove_entregador.html',
        entregadores=EntregadoService.visu()
    )
