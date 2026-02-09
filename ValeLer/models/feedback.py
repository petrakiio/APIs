from connection import feedback_conn

class Feedback:
    def __init__(self, nome, gmail, mensagem):
        self.nome = nome
        self.gmail = gmail
        self.mensagem = mensagem

class FeedbackService:
    
    @staticmethod
    def enviar_feedback(feedback:Feedback):
        if not feedback.nome or not feedback.gmail or not feedback.mensagem:
            return False, "Todos os campos são obrigatórios."
        
        if len(feedback.nome) < 3:
            return False, "O nome deve conter pelo menos 3 caracteres."
        
        if len(feedback.gmail) < 5 or "@" not in feedback.gmail:
            return False, "Email inválido."
        
        if len(feedback.mensagem) < 10:
            return False, "A mensagem deve conter pelo menos 10 caracteres."

        return feedback_conn.inserir_feedback(feedback), "Feedback enviado com sucesso."
    
    @staticmethod
    def listar_feedbacks():
        return feedback_conn.get_all_feedbacks()
    
    @staticmethod
    def deletar_feedback(id):
        return feedback_conn.deletar_feedback(id)