from connection import conn

class PessoaEmprestimo():
    def __init__(self, id_emprestimo, id_livro, nome_pessoa, data_emprestimo, data_devolucao, valor):
        self.id_emprestimo = id_emprestimo
        self.id_livro = id_livro
        self.nome_pessoa = nome_pessoa
        self.data_emprestimo = data_emprestimo
        self.data_devolucao = data_devolucao
        self.valor = valor

class EmprestimoService():
    
    @staticmethod
    def home() -> dict:
        return conn.get_emprestimos()
    
    @staticmethod
    def insert(emprestimo:PessoaEmprestimo):
        return conn.insert_emprestimos(emprestimo)

    @staticmethod
    def delete(id):
        r = conn.devolver_emprestimo(id)
        return r
    @staticmethod
    def delete_livro(id):
        r = conn.delete_book(id)
        return r