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
    db = None
    try:
        db = get_connection()
        cursor = db.cursor()
        sql = 'SELECT id FROM clientes WHERE email = %s'
        cursor.execute(sql, (email,))
        resultado = cursor.fetchone()
        return resultado is not None
        
    except Exception as err:
        print(f'Erro ao verificar e-mail: {err}')
        return False
    finally:
        if db:
            cursor.close()
            db.close()


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
    if not db:
        return None
    try:
        with db.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = """
                SELECT id, usuario, senha, foto_perfil, is_admin
                FROM clientes
                WHERE usuario = %s
            """
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

def deletar(id: int, user: str) -> bool:
    db = None
    try:
        db = get_connection()
        cursor = db.cursor()
        
        sql_carrinho = "DELETE FROM carrinho WHERE usuario_id = %s"
        cursor.execute(sql_carrinho, (id,))
        
        sql_usuario = "DELETE FROM clientes WHERE id = %s AND usuario = %s"
        cursor.execute(sql_usuario, (id, user))
        
        db.commit()
        return True
    except Exception as err:
        print(f"Erro no banco: {err}")
        return False
    finally:
        if db:
            db.close()
            
def get_user_id(nome_usuario):
    db = get_connection()
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT id FROM clientes WHERE usuario = %s", (nome_usuario,))
            res = cursor.fetchone()
            
            if res:
                return res.get('id') if isinstance(res, dict) else res[0]
            return None
    finally:
        db.close()

def get_itens_carrinho(user_nome):
    user_id = get_user_id(user_nome)
    try:
        db = get_connection()
        with db.cursor() as cursor:
            sql = "SELECT produto_id FROM carrinho WHERE usuario_id = %s"
            cursor.execute(sql, (user_id,))
            resultados = cursor.fetchall()
            
            if resultados and isinstance(resultados[0], dict):
                return [linha['produto_id'] for linha in resultados]
            return [linha[0] for linha in resultados]
    except Exception as e:
        print(f"Erro ao listar: {e}")
        return []
    finally:
        db.close()

def add_carinho(user_nome: str, item_id: int) -> bool:
    user_id = get_user_id(user_nome) 
    if not user_id: return False
    
    try:
        db = get_connection()
        cursor = db.cursor()
        sql = "INSERT INTO carrinho (usuario_id, produto_id, quantidade) VALUES (%s, %s, 1)"
        cursor.execute(sql, (user_id, item_id))
        db.commit()
        return True
    except Exception as e:
        print(f"Erro no INSERT: {e}")
        return False
    finally:
        db.close()

def del_carinho(user_nome, item_id):
    user_id = get_user_id(user_nome)
    try:
        db = get_connection()
        cursor = db.cursor()
        sql = "DELETE FROM carrinho WHERE usuario_id = %s AND produto_id = %s LIMIT 1"
        cursor.execute(sql, (user_id, item_id))
        db.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro no DELETE: {e}")
        return False
    finally:
        db.close()
def add_com(user, comentario, nota):
    db = None
    try:
        db = get_connection()
        cursor = db.cursor()
        sql = 'INSERT INTO feedback(usuario_id, comentario, nota) VALUES (%s, %s, %s)'
        cursor.execute(sql, (user, comentario, nota))
        db.commit()
        cursor.close()
        return True
    except Exception as e:
        print(f"Erro ao inserir feedback: {e}")
        return False
    finally:
        if db:
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

#Admin methods
def feeds():
    db = None
    try:
        db = get_connection()
        cursor = db.cursor(pymysql.cursors.DictCursor)
        sql = 'SELECT * FROM feedback'
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print('Erro:', e)
        return []
    finally:
        if db is not None:
            db.close()


def deletar(feedback_id):
    db = None
    try:
        db = get_connection()
        cursor = db.cursor()
        sql = 'DELETE FROM feedback WHERE id = %s'
        cursor.execute(sql, (feedback_id,))
        db.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print('Erro:', e)
        return False
    finally:
        if db is not None:
            db.close()

def users_get():
    db = None
    try:
        db = get_connection()
        cursor = db.cursor()
        sql = 'SELECT * FROM clientes'
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as err:
        print('Erro:',err)
        return None
    finally:
        if db is not None:
            db.close()

def users_del(id):
    db = None
    try:
        db = get_connection()
        cursor = db.cursor()
        sql = 'DELETE FROM clientes WHERE id = %s'
        cursor.execute(sql,(id))
        return True
    except Exception as err:
        print('Erro:',err)
        return False
    finally:
        if db is not None:
            db.close()

def users_admin(id):
    db = None
    try:
        db = get_connection()
        cursor = db.cursor()
        sql = 'UPDATE clientes SET is_admin = 1 WHERE id = %s'
        cursor.execute(sql,(id))
        return True
    except Exception as err:
        print('Erro:',err)
    finally:
        if db is not None:
            db.close()