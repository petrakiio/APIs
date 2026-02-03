from connection import conn

class Livro:
    def __init__(self, titulo, autor, editora, ano_publicacao, isbn, categoria, total_unidades, unidades_disponiveis):
        self.titulo = titulo
        self.autor = autor
        self.editora = editora
        self.ano_publicacao = ano_publicacao
        self.isbn = isbn
        self.categoria = categoria
        self.total_unidades = total_unidades
        self.unidades_disponiveis = unidades_disponiveis


class BibliotecaService():

    @staticmethod
    def home() -> dict:
        return conn.get_books()
    
    @staticmethod
    def insert(book:Livro):
        return conn.insert_books(book)
    