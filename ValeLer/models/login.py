from connection import login_conn

class Pessoa:
    def __init__(self, nome, gmail, senha, is_admin):
        self.nome = nome
        self.gmail = gmail
        self.senha = senha
        self.is_admin = is_admin

class PessoaService:
    INVALID_LOGIN_MESSAGE = "Credenciais inválidas."

    @staticmethod
    def cadastrar(user:Pessoa):
        if not user.nome or not user.gmail or not user.senha:
            return False, "Todos os campos são obrigatórios."
        
        if login_conn.get_usuario_por_nome(user.nome):
            return False, "Usuário já existe."
        
        if login_conn.get_usuario_por_gmail(user.gmail):
            return False, "Email já cadastrado."
        
        if len(user.senha) < 6:
            return False, "A senha deve conter pelo menos 6 caracteres."
        
        if len(user.nome) < 3:
            return False, "O nome deve conter pelo menos 3 caracteres."
        
        if len(user.gmail) < 5 or "@" not in user.gmail:
            return False, "Email inválido."

        return login_conn.insert_usuario(user), "Usuário cadastrado com sucesso."
    
    @staticmethod
    def login(gmail, senha):
        if not gmail or not senha:
            return False, "Todos os campos são obrigatórios."
        
        usuario = login_conn.get_usuario_por_gmail(gmail)
        if not usuario:
            return False, PessoaService.INVALID_LOGIN_MESSAGE
        
        if not login_conn.buscar_senha(senha, usuario['password']):
            return False, PessoaService.INVALID_LOGIN_MESSAGE
        
        return True, "Login bem-sucedido.", usuario
