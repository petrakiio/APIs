from flask import Blueprint, render_template,request,flash,url_for,redirect
from routes.auth import admin_required, entregador_required
from routes.tools import tratamento_dados
from models.entregador_class import Entregador,EntregadoService
from models.registro_class import Registro,RegistroService
import os

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
    if request.method == ['POST']:
        nome =  request.form.get('nome')
        entregador = Entregador(
        nome = tratamento_dados(nome),
        user = request.form.get('usuario'),
        email = request.form.get('email'),
        telefone = request.form.get('telefone'),
        veiculo = request.form.get('veiculo'),
        placa = request.form.get('placa'),
        ativar = True
        )
        if entregador is None:
            return flash('Complete os Dados')
        
        r = EntregadoService.add(entregador)
        if r:
            flash('Entregador adicionado com sucesso!')
            return redirect(url_for('entregador.visualizar'))
        flash('Erro ao adicionar entregado:(')
        return redirect(url_for('entregador.painel_entregador'))


    return render_template('admin_add_entregador.html')


@entregador_route.route('/admin_entregador/visualizar')
@admin_required
def admin_view_entregador():
    return render_template('admin_view_entregador.html',entregadores=EntregadoService.visu())


@entregador_route.route('/admin_entregador/remover',methods=['POST', 'GET'])
@admin_required
def admin_remove_entregador():
    if request.method == 'POST':
       registro = Registro(
        nome = request.form.get('nome'),
        motivo = request.form.get('motivo'),
        obs = request.form.get('observacao')
       )
       r = RegistroService.add_m(registro)
       if r:
        nome = tratamento_dados(registro.nome)
        
    return render_template('admin_remove_entregador.html')
