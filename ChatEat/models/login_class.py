from routes.tools import validar_idade,get_client_ip,pode_tentar_login
from connection.auth_conn import (
    inserir_cliente,
    buscar_cliente,
    buscar_senha,
    verificar_email,
    criptografar_senha,
    deletar,
    atualizar_imagem_perfil,
    get_email,
    update_password
)

class Pessoa:
    def __init__(self,nome,senha,email,data):
        self.nome = nome
        self.senha = senha
        self.email = email
        self.data = data
    

class PersonaService():
    @staticmethod
    def cadastrar(pessoa: Pessoa):

        if not all([pessoa.nome, pessoa.senha, pessoa.email, pessoa.data]):
            return 'Por favor, preencha todos os campos.'

        if not validar_idade(18, pessoa.data):
            return 'Você deve ter pelo menos 18 anos para se cadastrar.'

        if verificar_email(pessoa.email):
            return 'Este e-mail já está em uso!'

        senha_hash = criptografar_senha(pessoa.senha)

        sucesso = inserir_cliente(
            pessoa.nome,
            senha_hash,
            pessoa.email,
            pessoa.data
        )

        return True if sucesso else False
    @staticmethod
    def login(pessoa: Pessoa):
        ip = get_client_ip()

        if not pode_tentar_login(ip):
            return {'ok': False, 'msg': 'Muitas tentativas, tente depois'}

        if len(pessoa.nome) > 50 or len(pessoa.senha) > 100:
            return {'ok': False, 'msg': 'Dados inválidos'}

        cliente = buscar_cliente(pessoa.nome)

        if not cliente:
            return {'ok': False, 'msg': 'Usuário não encontrado'}

        if not buscar_senha(pessoa.senha, cliente['senha']):
            return {'ok': False, 'msg': 'Senha incorreta'}

        return {'ok': True, 'cliente': cliente}


    #Metodos de Perfil

    @staticmethod
    def deletar_method(usuario_id):
        cliente = buscar_cliente(usuario_id)
        user = cliente['usuario']
        sucesso = deletar(usuario_id)
        return sucesso
    
    @staticmethod
    def atulizar(usuario_id, imagem_path):
        sucesso = atualizar_imagem_perfil(usuario_id, imagem_path)
        return sucesso

    @staticmethod
    def get_em(email):
        id = get_email(email)
        return id
    
    @staticmethod
    def atualizar_password(password,id):
        result = update_password(id,password)
        if result:
            {'msg':'Senha atualizada com sucesso!'}