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