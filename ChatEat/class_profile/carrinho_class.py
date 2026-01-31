from connection.conn import add_carinho,del_carinho,get_itens_carrinho
from routes.itens import products

class CarrinhoService():
    @staticmethod
    def listar(user):
        if not user:
            return {'ok': False, 'msg': 'Usuário inválido'}

        ids_no_banco = get_itens_carrinho(user)

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
        for produto in products:
            if produto['id'] == id:
                if add_carinho(nome,id):
                    return {'ok': True,'msg':'Produto adicionado ao carrinho'}
                else:
                    return {'ok':False,'msg':'Erro ao adicionar o produto'}
        return {'ok': None,'msg':'produto não encontrado'}