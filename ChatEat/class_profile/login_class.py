from routes.tools import validar_idade
from connection.conn import inserir_cliente,buscar_cliente,buscar_senha,verificar_email,criptografar_senha

class Pessoa():
    def __init__(self,nome,senha,email,data):
        self.nome = nome
        self.senha = senha
        self.email = email
        self.data = data
    

class PersonaService():
    @staticmethod
    def cadastrar(pessoa: Pessoa):

        if not all([pessoa.nome, pessoa.senha, pessoa.email, pessoa.data]):
            return 'Por favor, preencha todos os campos.',False

        if not validar_idade(18, pessoa.data):
            return 'Você deve ter pelo menos 18 anos para se cadastrar.',False

        if verificar_email(pessoa.email):
            return 'Este e-mail já está em uso!',False

        senha_hash = criptografar_senha(pessoa.senha)

        sucesso = inserir_cliente(
            pessoa.nome,
            senha_hash,
            pessoa.email,
            pessoa.data
        )

        return True if sucesso else False