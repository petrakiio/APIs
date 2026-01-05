from conn import cursor
import random

def gerar_codigo_pedido():
    return str(random.randint(100000, 999999))


def inserir_pedido(nome,preco,codigo):
    try:
        cursor.execute("INSERT INTO pedidos (nome, preco, codigo) VALUES (%s, %s, %s)", (nome, preco, codigo))
        cursor.connection.commit()
        return True
    except Exception as e:
        print(f"Erro ao inserir pedido: {e}")
        return False
