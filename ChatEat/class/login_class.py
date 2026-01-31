from routes.tools import validar_idade


class Pessoa():
    def __init__(self,nome,senha,email,data):
        self.nome = nome
        self.senha = senha
        self.email = email
        self.data = data
    def cadastro(self):
        

class PersonaService():
    @staticmethod
    def verificar():