from flask import Blueprint,session,redirect,render_template,url_for,flash
from models.carrinho_class import CarrinhoService
from models.produtos_class import Product
from routes.auth import login_required

carrinho_route = Blueprint('carrinho',__name__)



@carrinho_route.route('/carinho')
@login_required
def carrinho():
    resultado = CarrinhoService.listar((session.get('usuario_nome')))
    if not resultado['ok']:
        flash(resultado['msg'], 'danger')
        return redirect(url_for('home.index'))

    return render_template(
        'carinho.html',
        carrinho=resultado['carrinho']
    )

@carrinho_route.route('/adicionar-carinho/<int:id>',methods=['POST'])
@login_required
def adicionar(id):
    r = CarrinhoService.add(id,session.get('usuario_nome'))
    if r['ok']:
        flash(r['msg'],'success')
    elif r['ok'] == None:
        flash(r['msg'],'danger')
    else:
        flash(r['msg'],'danger')
    return redirect(url_for('home.index'))

@carrinho_route.route('/remover-carinho/<int:id>')
@login_required
def deletar_item(id):
    r = CarrinhoService.dell(session.get('usuario_nome'),id)
    if r['ok']:
        flash(r['msg'],'success')
    else:
        flash(r['msg'],'danger')
    return redirect(url_for('carrinho.carrinho'))

@carrinho_route.route('/confirmar-compra', methods=['POST'])
@login_required
def confirmar_compra():
    flash('Checkout ainda não implementado.', 'danger')
    return redirect(url_for('home.index'))
