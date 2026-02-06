from flask import Blueprint,render_template,redirect,url_for,request,flash
from models.gatway_class import Gatway,GatwayService

gatway_route = Blueprint('gatway', __name__)

@gatway_route.route('/iniciar_pagamento/<int:id>')
def iniciar_pagamento(id):
    pass


@gatway_route.route('/sucesso')
def compra_sucesso():
    return render_template('compra_sucesso.html')


@gatway_route.route('/falha')
def compra_falha():
    return render_template('compra_falha.html')


@gatway_route.route('/pendente')
def compra_pendente():
    return render_template('compra_pendente.html')
