from connection.cart_conn import add_carinho, del_carinho, get_itens_carrinho
from models.produtos_class import Product
from routes.tools import tratamento_dados

class CarrinhoService:
    @staticmethod
    def listar(user):
        if not user:
            return {'ok': False, 'msg': 'Usuário inválido'}

        user = tratamento_dados(user)

        ids_no_banco = get_itens_carrinho(user)
        products = Product.get_all_products()
        carrinho_completo = []
        for p_id in ids_no_banco:
            for p in products:
                if p['id'] == p_id:
                    carrinho_completo.append(p)
                    break

        return {
            'ok': True,
            'carrinho': carrinho_completo
        }
    
    @staticmethod
    def add(id,nome):
        Product.get_product_by_id(id)
        if not Product.get_product_by_id(id):
            return {'ok':None,'msg':'Produto não encontrado'}
        resultado = add_carinho(nome,id)
        if resultado:
            return {'ok':True,'msg':'Item adicionado ao carrinho com sucesso!'}
        else:
            return {'ok':False,'msg':'Erro ao adicionar o item ao carrinho'}
    
    @staticmethod
    def dell(user,id):
        resultado = del_carinho(user,id)
        if resultado:
            return {'ok':True,'msg':'Item deletado com sucesso!'}
        else:
            return {'ok':False,'msg':'Erro ao deletar o item'}
