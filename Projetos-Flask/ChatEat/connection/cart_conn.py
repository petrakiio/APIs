from .core import get_connection


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
    if not user_id:
        return False
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
