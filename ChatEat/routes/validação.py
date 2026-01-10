import secrets
import string
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()

# No seu .env, coloque o USERNAME e PASSWORD que o Mailtrap te deu na tela de SMTP
user_mailtrap = os.getenv('MAILTRAP_USER')
pass_mailtrap = os.getenv('MAILTRAP_PASS')

def criar_codigo() -> str:
    caracteres = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(caracteres) for _ in range(6))

def enviar_codigo(codigo: str, email_usr: str):
    try:
        msg = EmailMessage()
        msg['Subject'] = 'Código de Verificação - ChatEat'
        msg['From'] = 'chateat21@gmail.com' 
        msg['To'] = email_usr
        
        msg.set_content(f"Seu código é: {codigo}")
        msg.add_alternative(f"""
            <html>
                <body style="font-family: sans-serif; text-align: center;">
                    <h2 style="color: #E21F26;">ChatEat</h2>
                    <p>Seu código de validação é:</p>
                    <div style="background: #F4F4F4; padding: 10px; font-size: 24px; font-weight: bold;">
                        {codigo}
                    </div>
                </body>
            </html>
        """, subtype='html')

        # Configuração SMTP do Mailtrap
        with smtplib.SMTP("sandbox.smtp.mailtrap.io", 2525) as server:
            server.login(user_mailtrap, pass_mailtrap)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Erro: {e}")
        return False
