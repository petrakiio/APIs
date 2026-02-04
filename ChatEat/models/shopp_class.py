from connection import conn

class Product:
    def __init__(self, id, nome, descricao, preco, img):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.img = img
    def get_all_products() -> dict:
        return conn.get_products()
    
    def search(term) -> list:
        return conn.search_products(term)
    
    def get_product_by_id(id) -> dict:
        products = conn.get_products()
        for product in products:
            if product['id'] == id:
                return product
        return None
    def delete_product(product_id: int) -> bool:
        r = conn.delete_product(product_id)
        if r:
            return {'ok':True,'msg':'Produto deletado com sucesso!'}
        else:
            return {'ok':False,'msg':'Erro ao deletar o produto'}