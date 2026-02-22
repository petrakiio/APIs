from flask import Blueprint
from routes.auth import login_required
from controllers import gatway_controller

gatway_route = Blueprint('gatway', __name__)

@gatway_route.route('/iniciar_pagamento/<int:id>',methods=['GET','POST'])
def iniciar_pagamento(id):
    return gatway_controller.iniciar_pagamento(id)


@gatway_route.route('/sucesso')
@login_required
def compra_sucesso():
    return gatway_controller.compra_sucesso()


@gatway_route.route('/falha')
@login_required
def compra_falha():
    return gatway_controller.compra_falha()


@gatway_route.route('/pendente')
@login_required
def compra_pendente():
    return gatway_controller.compra_pendente()

@gatway_route.route('/pagar_entregador/<int:id>', methods=['GET', 'POST'])
@login_required
def pagar_entregador(id):
    return gatway_controller.pagar_entregador(id)


@gatway_route.route('/caminho_entrega/<int:id>')
@login_required
def caminho_entrega_real(id):
    return gatway_controller.caminho_entrega_real(id)

@gatway_route.route('/webhook/mercadopago', methods=['POST'])
def webhook_mercadopago():
    return gatway_controller.webhook_mercadopago()
