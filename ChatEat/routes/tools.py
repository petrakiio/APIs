from flask import request
import datetime
import time

def validar_idade(data_nascimento_str, idade_minima):
    try:
        data_nasc = datetime.strptime(data_nascimento_str, '%Y-%m-%d')
        hoje = datetime.today()
        idade = hoje.year - data_nasc.year - ((hoje.month, hoje.day) < (data_nasc.month, data_nasc.day))
        return idade >= idade_minima
    except Exception as e:
        print(f"Erro na data: {e}")
        return False
    

MAX_TENTATIVAS = 5
BLOQUEIO_TEMPO = 300  
login_attempts = {}
ip_last_order = {}


def get_client_ip():
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0]
    return request.remote_addr

def pode_tentar_login(ip):
    dados = login_attempts.get(ip)
    if not dados:
        return True
    tentativas, ultimo_erro = dados
    if tentativas >= MAX_TENTATIVAS:
        if time() - ultimo_erro < BLOQUEIO_TEMPO:
            return False
        else:
            del login_attempts[ip]
    return True

def registrar_erro_login(ip):
    if ip not in login_attempts:
        login_attempts[ip] = [1, time()]
    else:
        login_attempts[ip][0] += 1
        login_attempts[ip][1] = time()

def resetar_tentativas(ip):
    login_attempts.pop(ip, None)
