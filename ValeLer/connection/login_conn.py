from connection.core import get_connection
import argon2

ph = argon2.PasswordHasher()

def criptografar_senha(senha):
    return ph.hash(senha)


def buscar_senha(senha: str, senha_hash: str) -> bool:
    try:
        ph.verify(senha_hash, senha)
        return True
    except argon2.exceptions.VerifyMismatchError:
        return False
    
def insert_usuario(usuario:object) -> bool:
    db = None
    try:
        db = get_connection()
        sql = "INSERT INTO clientes_Valeler (nome, gmail, password, is_admin) VALUES (%s, %s, %s, %s)"
        cursor = db.cursor()
        cursor.execute(sql, (
            usuario.nome,
            usuario.gmail,
            criptografar_senha(usuario.senha),
            usuario.is_admin
        ))
        db.commit()
        return True
    except Exception as err:
        print('Erro:',err)
    finally:
        if db is not None:
            db.close()

def get_usuario_por_gmail(gmail):
    db = None
    try:
        db = get_connection()
        cursor = db.cursor()
        sql = 'SELECT * FROM clientes_Valeler WHERE gmail = %s LIMIT 1'
        cursor.execute(sql, (gmail,))
        return cursor.fetchone()
    except Exception as erro:
        print('Erro:',erro)
        return None
    finally:
        if db is not None:
            db.close()

def get_usuario_por_nome(nome):
    db = None
    try:
        db = get_connection()
        cursor = db.cursor()
        sql = 'SELECT * FROM clientes_Valeler WHERE nome = %s LIMIT 1'
        cursor.execute(sql, (nome,))
        return cursor.fetchone()
    except Exception as erro:
        print('Erro:',erro)
        return None
    finally:
        if db is not None:
            db.close()
