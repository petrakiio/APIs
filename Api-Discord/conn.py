import pymysql
from dotenv import load_dotenv
import os
import argon2
load_dotenv()

try:
    connection = pymysql.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        port=int(os.getenv('DB_PORT'))
    )
    cursor = connection.cursor()
    print("Conexão bem-sucedida ao banco de dados!")
except Exception as e:
    print(f"Erro ao conectar ao banco de dados: {e}")

def criptografar_senha(senha):
    ph = argon2.PasswordHasher()
    return ph.hash(senha)

def inserir_cliente(usuario,senha,email,data):
    try:
        sql = "INSERT INTO clientes (usuario,senha,email,data_nascimento) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (usuario, senha, email, data))
        connection.commit()
        print("Cliente inserido com sucesso!")
        return True
    except Exception as e:
        print(f"Erro ao inserir cliente: {e}")
        return False

def buscar_cliente(usuario,email):
    try:
        sql = "SELECT * FROM clientes WHERE usuario = %s AND email = %s"
        cursor.execute(sql, (usuario, email))
        result = cursor.fetchone()
        return result
    except Exception as e:
        print(f"Erro ao buscar cliente: {e}")
        return None