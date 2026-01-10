from connection.conn import get_connection
import random

def gerar_codigo_pedido():
    return random.randint(100000, 999999)

def inserir_pedido(nome, codigo):
    db = get_connection() 
    if not db: return False
    try:
        with db.cursor() as cursor:
            sql = "INSERT INTO pedidos (nome, codigo) VALUES (%s, %s)"
            cursor.execute(sql, (nome, codigo))
            db.commit()
            return True
    except Exception as e:
        print(f"Erro ao inserir pedido: {e}")
        return False
    finally:
        db.close() 

def consultar_pedido_db(codigo):
    db = get_connection()
    if not db: return None
    try:
        with db.cursor() as cursor:
            sql = "SELECT nome FROM pedidos WHERE codigo = %s"
            cursor.execute(sql, (codigo,))
            return True
    except Exception as e:
        print(f"Erro ao consultar pedido: {e}")
        return None
    finally:
        db.close()

def pedido_entrege(codigo):
    db = get_connection()
    if not db: return False
    try:
        with db.cursor() as cursor:
            sql = "DELETE FROM pedidos WHERE codigo = %s"
            cursor.execute(sql, (codigo,))
            db.commit()
            return cursor.rowcount > 0 # Retorna True se deletou algo
    except Exception as e:
        print(f"Erro ao marcar pedido como entregue: {e}")
        return False
    finally:
        db.close()