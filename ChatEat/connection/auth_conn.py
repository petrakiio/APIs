import argon2
from .core import get_connection

ph = argon2.PasswordHasher()


def criptografar_senha(senha):
    return ph.hash(senha)


def buscar_senha(senha: str, senha_hash: str) -> bool:
    try:
        ph.verify(senha_hash, senha)
        return True
    except argon2.exceptions.VerifyMismatchError:
        return False


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
    if not db:
        return False
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
        with db.cursor() as cursor:
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


def atualizar_imagem_perfil(usuario_id, img_url):
    db = get_connection()
    if not db:
        return False
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
