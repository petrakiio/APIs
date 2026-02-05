from .core import get_connection


def get_products():
    db = None
    try:
        db = get_connection()
        cursor = db.cursor()
        sql = 'SELECT * FROM products'
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print('Erro ao buscar produtos:', e)
        return []
    finally:
        if db is not None:
            db.close()


def search_products(term: str):
    db = None
    try:
        db = get_connection()
        cursor = db.cursor()
        like = f"%{term}%"
        sql = """
            SELECT * FROM products
            WHERE nome LIKE %s OR descricao LIKE %s
        """
        cursor.execute(sql, (like, like))
        return cursor.fetchall()
    except Exception as e:
        print('Erro ao buscar produtos por termo:', e)
        return []
    finally:
        if db is not None:
            db.close()


def delete_product(product_id: int) -> bool:
    db = None
    try:
        db = get_connection()
        cursor = db.cursor()
        sql = 'DELETE FROM products WHERE id = %s'
        cursor.execute(sql, (product_id,))
        db.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print('Erro ao deletar produto:', e)
        return False
    finally:
        if db is not None:
            db.close()


def insert_product(produto) -> bool:
    db = None
    try:
        db = get_connection()
        cursor = db.cursor()
        sql = 'INSERT INTO products (nome, descricao, preco, img) VALUES (%s, %s, %s, %s)'
        cursor.execute(
            sql,
            (produto.nome, produto.descricao, produto.preco, produto.img)
        )
        db.commit()
        return True
    except Exception as e:
        print('Erro ao inserir produto:', e)
        return False
    finally:
        if db is not None:
            db.close()


def update_product(produto) -> bool:
    db = None
    try:
        db = get_connection()
        cursor = db.cursor()
        sql = 'UPDATE products SET nome = %s, descricao = %s, preco = %s, img = %s WHERE id = %s'
        cursor.execute(
            sql,
            (produto.nome, produto.descricao, produto.preco, produto.img, produto.id)
        )
        db.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print('Erro ao atualizar produto:', e)
        return False
    finally:
        if db is not None:
            db.close()
