from conn import cursor
import random

def gerar_codigo_pedido():
    return random.randint(100000, 999999)


def inserir_pedido(nome,preco,codigo):
    try:
        sql = "INSERT INTO pedidos (nome, preco, codigo) VALUES (%s, %s, %s)"
        cursor.execute(sql,(nome, preco, codigo))
        cursor.connection.commit()
        return True
    except Exception as e:
        print(f"Erro ao inserir pedido: {e}")
        return False
    
def consultar_pedido_db(codigo):
    try:
        sql = "SELECT nome, preco FROM pedidos WHERE codigo = %s"
        cursor.execute(sql, (codigo,))
        pedido = cursor.fetchone()
        return True
    except Exception as e:
        print(f"Erro ao consultar pedido: {e}")
        return None

def pedido_entrege(codigo):
    try:
        sql = "DELETE FROM pedidos WHERE codigo = %s"
        cursor.execute(sql, (codigo,))
        cursor.connection.commit()
        return True
    except Exception as e:
        print(f"Erro ao marcar pedido como entregue: {e}")
        return False
    