from flask import Blueprint,render_template,redirect,url_for,request,flash
from connection import gatway_conn
from models.gatway_class import Gatway,GatwayService
from routes.auth import login_required
from models.produtos_class import Product

gatway_route = Blueprint('gatway', __name__)

@gatway_route.route('/iniciar_pagamento/<int:id>',methods=['GET','POST'])
def iniciar_pagamento(id):
    url_pagamento = GatwayService.criar_gatway(id)
    if not url_pagamento:
        flash("Erro ao criar pagamento. Tente novamente.")
        return redirect(url_for('home.index'))
    GatwayService.gerar_qr_code(url_pagamento)
    return render_template('pagamento.html',product=Product.get_product_by_id(id))


@gatway_route.route('/sucesso')
@login_required
def compra_sucesso():
    payment_id = request.args.get('payment_id') or request.args.get('collection_id')
    if payment_id:
        status = gatway_conn.get_payment_status(payment_id)
        if status and status != "approved":
            return redirect(url_for('gatway.compra_pendente'))
    return render_template('compra_sucesso.html')


@gatway_route.route('/falha')
@login_required
def compra_falha():
    if not GatwayService.deletar_qr_code():
        print("Erro ao deletar o QR code.")
    return render_template('compra_falha.html')


@gatway_route.route('/pendente')
@login_required
def compra_pendente():
    return render_template('compra_pendente.html')

@gatway_route.route('/webhook/mercadopago', methods=['POST'])
def webhook_mercadopago():
    payload = request.get_json(silent=True) or {}
    payment_id = None

    data = payload.get("data") or {}
    if isinstance(data, dict):
        payment_id = data.get("id")

    if not payment_id:
        payment_id = request.args.get("data.id")

    if payment_id:
        status = gatway_conn.get_payment_status(payment_id)
        if status:
            gatway_conn.set_payment_status(payment_id, status)

    return "", 200
