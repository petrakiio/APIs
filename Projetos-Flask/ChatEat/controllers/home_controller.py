from flask import render_template, request, redirect, url_for
from models.produtos_class import Product


def index():
    products = Product.get_all_products()
    return render_template("index.html", products=products)


def search():
    term = request.form.get("search_term", "")
    resultados = Product.search(term)
    return render_template("index.html", products=resultados)


def sobre():
    return render_template("sobre.html")


def status_entrega():
    return render_template("status_entrega.html")


def products_page(id):
    product_found = Product.get_product_by_id(id)
    if product_found:
        return render_template("comprar.html", product=product_found)
    return redirect(url_for("home.index"))
