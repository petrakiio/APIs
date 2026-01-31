from connection.conn import add_com

class FeedbackService():
    @staticmethod
    def enviar(user,comentario,nota):
        if not comentario or len(comentario) > 5:
            return {'ok': False,'msg':'Mensaguem Inválida'}
        if not user or not comentario or nota is None:
            return {'ok': False, 'msg': 'Falta de Dados'}
        resultado = add_com(user,comentario,nota)
        if resultado:
            return {'ok':True,'msg':'Seu Comentario foi enviado e recebido com sucesso!obrigado por avaliar'}
        else:
            return {'ok': False, 'msg':'Infelizmente tivemos um erro ao enviar seu comentario :(,tente novamente mais tarde'}
        