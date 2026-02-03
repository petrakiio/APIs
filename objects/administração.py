from connection import conn

class BibliotecaService():

    @staticmethod
    def home() -> dict:
        return conn.get_books()