from connection import gatway_conn
from models.produtos_class import Product

class Gatway:
    def __init__(self, id, nome, descricao, preco):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.preco = preco

class GatwayService:
    @staticmethod
    def criar_gatway(id):
        id_produto = Product.get_product_by_id(id)
        if not id_produto:
            return None
        
        produto = Gatway(
            id=id_produto['id'],
            nome=id_produto['nome'],
            descricao=id_produto['descricao'],
            preco=id_produto['preco']
        )
        return gatway_conn.create_gatway(produto)
    
    @staticmethod
    def gerar_qr_code(url):
        return gatway_conn.generate_qr_code(url)

    @staticmethod
    def deletar_qr_code():
        return gatway_conn.delete_qr_code()