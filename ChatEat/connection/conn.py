import pymysql
from dotenv import load_dotenv
import os
import argon2

load_dotenv()
ph = argon2.PasswordHasher()

def get_connection():
    try:
        return pymysql.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            port=int(os.getenv('DB_PORT')),
            cursorclass=pymysql.cursors.DictCursor 
        )
    
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def criptografar_senha(senha):
    return ph.hash(senha)

def verificar_email(email):
    try:
        db = get_connection()
        cursor = db.cursor()
        sql = 'SELECT id FROM clientes WHERE email = %s'
        cursor.execute(sql, (email,))
        resultado = cursor.fetchall()
        return resultado is not None
    except Exception as err:
        print(f'erro:{err}')
        return False
    finally:
        db.close()
        cursor.close()


def inserir_cliente(usuario, senha, email, data):
    db = get_connection()
    if not db: return False
    try:
        with db.cursor() as cursor:
            sql = "INSERT INTO clientes (usuario, senha, email, data_nascimento) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (usuario, senha, email, data))
        db.commit()
        print("Cliente inserido com sucesso!")
        return True
    except Exception as e:
        print(f"Erro ao inserir cliente: {e}")
        return False
    finally:
        db.close() 

def buscar_cliente(usuario):
    db = get_connection()
    if not db: return None
    try:
        with db.cursor() as cursor:
            sql = "SELECT id, usuario, senha, foto_perfil FROM clientes WHERE usuario = %s"
            cursor.execute(sql, (usuario,))
            return cursor.fetchone()
    except Exception as e:
        print(f"Erro ao buscar cliente: {e}")
        return None
    finally:
        db.close()
def buscar_senha(senha: str,senha_hash: str)-> bool:
    try:
        ph.verify(senha_hash, senha)
        return True
    except argon2.exceptions.VerifyMismatchError:
        return False

def deletar(id,user):
    try:
        db = get_connection()
        cursor = db.cursor()
        sql = "DELETE FROM clientes WHERE id = %s AND usuario = %s"
        valores = id,user
        cursor.execute(sql,valores)
        db.commit()
        return True
    except Exception as err:
        print(f'Error:{err}')
        return False
    finally:
        db.close()

def add_carinho(user,item):
    try:
        db = get_connection()
        cursor = db.cursor()
        sql = 'UPDATE clientes SET carinho = %s WHERE usuario = %s'
        cursor.execute(sql(item,user))
        return cursor.fetchall()
    except Exception as e:
        return f'erro:{e}'
    finally:
        db.close()
        
def atualizar_imagem_perfil(usuario_id, img_url):
    db = get_connection()
    if not db: return False
    try:
        with db.cursor() as cursor:
            sql = "UPDATE clientes SET foto_perfil = %s WHERE id = %s"
            cursor.execute(sql, (img_url, usuario_id))
        db.commit()
        return True
    except Exception as e:
        print(f"Erro ao atualizar imagem de perfil: {e}")
        return False
    finally:
        db.close()