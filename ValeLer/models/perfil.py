from connection import perfil_conn as conn

class PerfilService:

    @staticmethod
    def update_img(id_usuario, img_path):
        return conn.atualizar_foto_usuario(id_usuario, img_path)
    
    @staticmethod
    def buscar_usuario(nome,gmail):
        return conn.devolucao(nome, gmail)
    
    @staticmethod
    def devolver_emprestimo(id_usuario):
        return conn.devolver_emprestimo(id_usuario)

    @staticmethod
    def get_emprestimo_por_nome(nome):
        return conn.get_emprestimo_por_nome(nome)
