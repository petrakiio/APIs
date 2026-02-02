from connection.conn import feeds,deletar,users_get,users_admin,users_del,users_rm_admin

class AdminService():
    @staticmethod
    def feedback():
        return feeds()
    
    @staticmethod
    def del_fed(feedback_id):
        r = deletar(feedback_id)
        if r:
            return {'ok':True,'msg':'Item removido!'}
        else:
            return {'ok':False,'msg':'Erro ao remover item'}
    
    @staticmethod
    def users():
        return users_get()
    
    @staticmethod
    def del_user(id):
        r = users_del(id)
        if r:
            return {'ok':True,'msg':'Usuario deletado com sucesso!'}
        else:
            return {'ok':True,'msg':'Erro ao deletar usuario'}
        
    @staticmethod
    def add_new_admin(id):
        r = users_admin(id)
        if r:
            return {'ok':True,'msg':'Admin Adicionado!'}
        else:
            return {'ok':True,'msg':'Erro ao conceder Adm'}

    @staticmethod
    def rm_admin