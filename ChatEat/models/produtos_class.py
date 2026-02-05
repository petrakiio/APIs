from connection import products_conn as conn

class Product:
    def __init__(self, id, nome, descricao, preco, img):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.img = img

    @staticmethod
    def get_all_products() -> list:
        return conn.get_products()
    
    @staticmethod
    def search(term: str) -> list:
        return conn.search_products(term)
    
    @staticmethod
    def get_product_by_id(id: int) -> dict:
        products = conn.get_products()
        return next((p for p in products if p['id'] == id), None)

    @staticmethod
    def delete_product(product_id: int) -> dict:
        r = conn.delete_product(product_id)
        if r:
            return {'ok': True, 'msg': 'Produto deletado com sucesso!'}
        return {'ok': False, 'msg': 'Erro ao deletar o produto'}
    
    @staticmethod
    def insert_product(nome: str, descricao: str, preco: float, img: str) -> dict:
        produto = Product(None, nome, descricao, preco, img)
        r = conn.insert_product(produto)
        if r:
            return {'ok': True, 'msg': 'Produto inserido com sucesso!'}
        return {'ok': False, 'msg': 'Erro ao inserir o produto'}

    @staticmethod
    def update_product(id: int, nome: str, descricao: str, preco: float, img: str) -> dict:
        produto = Product(id, nome, descricao, preco, img)
        r = conn.update_product(produto)
        if r:
            return {'ok': True, 'msg': 'Produto atualizado com sucesso!'}
        return {'ok': False, 'msg': 'Erro ao atualizar o produto'}  
