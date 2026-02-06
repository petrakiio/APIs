from flask import Blueprint,render_template,redirect,url_for,request,flash
from models.gatway_class import Gatway,GatwayService
from models.produtos_class import Product

gatway_route = Blueprint('gatway', __name__)

@gatway_route.route('/iniciar_pagamento/<int:id>',methods=['GET','POST'])
def iniciar_pagamento(id):
    url_pagamento = GatwayService.criar_gatway(id)
    if not url_pagamento:
        flash("Erro ao criar pagamento. Tente novamente.")
        return redirect(url_for('home.home'))
    GatwayService.gerar_qr_code(url_pagamento)
    return render_template('pagamento.html',product=Product.get_product_by_id(id))


@gatway_route.route('/sucesso')
def compra_sucesso():
    return render_template('compra_sucesso.html')


@gatway_route.route('/falha')
def compra_falha():
    return render_template('compra_falha.html')


@gatway_route.route('/pendente')
def compra_pendente():
    return render_template('compra_pendente.html')
