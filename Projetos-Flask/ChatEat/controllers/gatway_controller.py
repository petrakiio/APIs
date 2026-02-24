from flask import render_template, redirect, url_for, request, flash
from connection import gatway_conn
from models.gatway_class import GatwayService
from models.produtos_class import Product


def iniciar_pagamento(id):
    url_pagamento = GatwayService.criar_gatway(id)
    if not url_pagamento:
        flash("Erro ao criar pagamento. Tente novamente.")
        return redirect(url_for("home.index"))

    GatwayService.gerar_qr_code(url_pagamento)
    return render_template("pagamento.html", product=Product.get_product_by_id(id))


def compra_sucesso():
    payment_id = request.args.get("payment_id") or request.args.get("collection_id")
    if payment_id:
        status = gatway_conn.get_payment_status(payment_id)
        if status and status != "approved":
            return redirect(url_for("gatway.compra_pendente"))
    return render_template("compra_sucesso.html")


def compra_falha():
    if not GatwayService.deletar_qr_code():
        print("Erro ao deletar o QR code.")
    return render_template("compra_falha.html")


def compra_pendente():
    return render_template("compra_pendente.html")


def pagar_entregador(id):
    product = Product.get_product_by_id(id)
    if not product:
        flash("Produto nao encontrado.", "error")
        return redirect(url_for("home.index"))

    if request.method == "POST":
        forma_pagamento = request.form.get("forma_pagamento", "dinheiro")
        return redirect(
            url_for(
                "gatway.caminho_entrega_real",
                id=id,
                forma_pagamento=forma_pagamento,
            )
        )

    return render_template("pagar_entregador.html", product=product)


def caminho_entrega_real(id):
    product = Product.get_product_by_id(id)
    if not product:
        flash("Produto nao encontrado.", "error")
        return redirect(url_for("home.index"))

    forma_pagamento = request.args.get("forma_pagamento", "dinheiro")
    return render_template(
        "caminho_entrega.html",
        product=product,
        forma_pagamento=forma_pagamento,
    )


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
