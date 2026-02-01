from connection.conn import feeds,deletar

class AdminService():
    @staticmethod
    def feedback():
        return feeds()
    
    @staticmethod
    def del_fed(feedback_id):
        r = deletar(feedback_id)
        if r:
            return {'ok':True,'msg':''}