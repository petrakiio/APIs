from connection.registro_conn import add_motivo

class Registro:
    def __init__(self,nome,mt,obs):
        self.nome = nome
        self.mt = mt
        self.obs = obs

class RegistroService:

    @staticmethod
    def add_m(registro:Registro):
        return add_motivo(registro)
