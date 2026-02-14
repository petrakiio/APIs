from connection.entregador_conn import get_entregador,add_entregador,rm_entregador

class Entregador:
    def __init__(self,nome,usuario,email,telefone,veiculo,placa,ativo):
        self.nome = nome
        self.usuario = usuario
        self.email = email
        self.telefone = telefone
        self.veiculo = veiculo
        self.placa = placa
        self.ativo = ativo

class EntregadoService:

    @staticmethod
    def visu():
        return get_entregador()
    
    @staticmethod
    def add(pessoa:Entregador):
        return add_entregador(pessoa)
    
    @staticmethod
    def rm(nome):
        if rm_entregador(nome):
            return True
        return False
