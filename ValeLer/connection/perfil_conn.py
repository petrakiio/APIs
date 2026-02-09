from connection.core import get_connection

def devolucao(nome: str, gmail: str) -> int | None:
    db = None
    try:
        db = get_connection()
        cursor = db.cursor()
        sql = 'SELECT id_cliente FROM clientes_Valeler WHERE nome = %s AND gmail = %s LIMIT 1'
        cursor.execute(sql, (nome, gmail))
        result = cursor.fetchone()
        return result['id_cliente'] if result else None
    except Exception as err:
        print('Erro:',err)
        return None
    finally:
        if db is not None:
            db.close()
def devolver_emprestimo(id_emprestimo) -> bool:
    db = None
    try:
        db = get_connection()
        cursor = db.cursor()
        sql_get_id_livro = "SELECT id_livro FROM emprestado WHERE id_emprestimo = %s"
        cursor.execute(sql_get_id_livro, (id_emprestimo,))
        result = cursor.fetchone()

        if not result:
            return False

        id_livro = result['id_livro']

        sql_update_livro = """
            UPDATE livros
            SET unidades_disponiveis = unidades_disponiveis + 1
            WHERE id_livro = %s
        """
        cursor.execute(sql_update_livro, (id_livro,))

        sql_delete_emprestimo = "DELETE FROM emprestado WHERE id_emprestimo = %s"
        cursor.execute(sql_delete_emprestimo, (id_emprestimo,))

        db.commit()
        return True

    except Exception as err:
        print('Erro:', err)
        if db:
            db.rollback()
        return False
    finally:
        if db is not None:
            db.close()

def get_emprestimo_por_nome(nome: str) -> int | None:
    db = None
    try:
        db = get_connection()
        cursor = db.cursor()
        sql = """
            SELECT id_emprestimo
            FROM emprestado
            WHERE nome_pessoa = %s
            ORDER BY data_emprestimo DESC, id_emprestimo DESC
            LIMIT 1
        """
        cursor.execute(sql, (nome,))
        result = cursor.fetchone()
        return result['id_emprestimo'] if result else None
    except Exception as err:
        print('Erro:', err)
        return None
    finally:
        if db is not None:
            db.close()

def atualizar_foto_usuario(id_usuario, img_url) -> bool:
    db = None
    try:
        db = get_connection()
        cursor = db.cursor()
        sql = "UPDATE clientes_Valeler SET img_user = %s WHERE id_cliente = %s"
        cursor.execute(sql, (img_url, id_usuario))
        db.commit()
        return True
    except Exception as err:
        print('Erro:', err)
        if db:
            db.rollback()
        return False
    finally:
        if db is not None:
            db.close()
