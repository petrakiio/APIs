from connection.conn import add_com

class FeedbackService:
    @staticmethod
    def enviar(user, comentario, nota):
        if not user or not comentario or nota is None:
            return {'ok': False, 'msg': 'Por favor, preencha todos os campos.'}

        if len(comentario) < 3:
            return {'ok': False, 'msg': 'O comentário é muito curto.'}

        resultado = add_com(user, comentario, nota)
        
        if resultado:
            return {'ok': True, 'msg': 'Seu comentário foi enviado com sucesso! Obrigado por avaliar.'}
        
        return {'ok': False, 'msg': 'Erro ao enviar comentário. Tente novamente mais tarde.'}