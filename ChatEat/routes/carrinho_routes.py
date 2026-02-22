from flask import Blueprint
from routes.auth import login_required
from controllers import carrinho_controller

carrinho_route = Blueprint('carrinho',__name__)

@carrinho_route.route('/carinho')
@login_required
def carrinho():
    return carrinho_controller.carrinho()

@carrinho_route.route('/adicionar-carinho/<int:id>',methods=['POST'])
@login_required
def adicionar(id):
    return carrinho_controller.adicionar(id)

@carrinho_route.route('/remover-carinho/<int:id>')
@login_required
def deletar_item(id):
    return carrinho_controller.deletar_item(id)

@carrinho_route.route('/confirmar-compra', methods=['POST'])
@login_required
def confirmar_compra():
    return carrinho_controller.confirmar_compra()
