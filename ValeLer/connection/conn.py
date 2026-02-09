from connection.core import get_connection
def get_books() -> dict | bool:
    db = None
    try:
        db = get_connection()
        cursor = db.cursor()
        sql = 'SELECT * FROM livros'
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as erro:
        print('Erro:',erro)
        return False
    finally:
        if db is not None:
            db.close()

def insert_books(livro) -> bool:
    db = None
    try:
        db = get_connection()
        sql = "INSERT INTO livros (titulo, autor, editora, ano_publicacao, isbn, categoria, total_unidades, unidades_disponiveis) " \
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor = db.cursor()
        cursor.execute(sql, (
            livro.titulo,
            livro.autor,
            livro.editora,
            livro.ano_publicacao,
            livro.isbn,
            livro.categoria,
            livro.total_unidades,
            livro.unidades_disponiveis
        ))
        db.commit()
        return True
    except Exception as err:
        print('Erro:',err)
    finally:
        if db is not None:
            db.close()

def get_emprestimos() -> dict:
    db = None
    try:
        db = get_connection()
        cursor = db.cursor()
        sql = """
            SELECT e.*, l.titulo AS titulo
            FROM emprestado e
            LEFT JOIN livros l ON l.id_livro = e.id_livro
        """
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as erro:
        print('Erro:', erro)
        return []
    finally:
        if db is not None:
            db.close()


def insert_emprestimos(emprestimo) -> bool:
    db = None
    try:
        db = get_connection()
        cursor = db.cursor()
        sql_update = """
            UPDATE livros
            SET unidades_disponiveis = unidades_disponiveis - 1
            WHERE id_livro = %s AND unidades_disponiveis > 0
        """
        cursor.execute(sql_update, (emprestimo.id_livro,))

        if cursor.rowcount == 0:
            db.rollback()
            return False

        sql_insert = """
            INSERT INTO emprestado
            (id_livro, nome_pessoa, data_emprestimo, data_devolucao, valor)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql_insert, (
            emprestimo.id_livro,
            emprestimo.nome_pessoa,
            emprestimo.data_emprestimo,
            emprestimo.data_devolucao,
            emprestimo.valor
        ))

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

def get_livros_usuario(nome_pessoa) -> dict:
    db = None
    try:
        db = get_connection()
        cursor = db.cursor()
        sql = """
            SELECT e.*, l.titulo AS titulo
            FROM emprestado e
            LEFT JOIN livros l ON l.id_livro = e.id_livro
            WHERE e.nome_pessoa = %s
        """
        cursor.execute(sql, (nome_pessoa,))
        return cursor.fetchall()
    except Exception as err:
        print('Erro:', err)
        return []
    finally:        
        if db is not None:
            db.close()

def delete_book(id_livro) -> bool:
    db = None
    try:
        db = get_connection()
        cursor = db.cursor()
        sql_check = "SELECT 1 FROM emprestado WHERE id_livro = %s LIMIT 1"
        cursor.execute(sql_check, (id_livro,))
        if cursor.fetchone():
            return False
        sql = "DELETE FROM livros WHERE id_livro = %s"
        cursor.execute(sql, (id_livro,))
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

def update_book(id_livro, livro) -> bool:
    db = None
    try:
        db = get_connection()
        cursor = db.cursor()
        sql = """
            UPDATE livros
            SET titulo = %s, autor = %s, editora = %s, ano_publicacao = %s, isbn = %s, categoria = %s, total_unidades = %s, unidades_disponiveis = %s
            WHERE id_livro = %s
        """
        cursor.execute(sql, (
            livro.titulo,
            livro.autor,
            livro.editora,
            livro.ano_publicacao,
            livro.isbn,
            livro.categoria,
            livro.total_unidades,
            livro.unidades_disponiveis,
            id_livro
        ))
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

def search_books(query) -> dict:
    db = None
    try:
        db = get_connection()
        cursor = db.cursor()
        sql = 'SELECT * FROM livros'
        cursor.execute(sql)
        livros = cursor.fetchall()
        for livro in livros:
            if query.lower() in livro['titulo'].lower():
                return livro
        return {}
    except Exception as err:
        print('Erro:', err)
        return {}
    finally:
        if db is not None:
            db.close()
