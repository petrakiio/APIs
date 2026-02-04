import pymysql
from dotenv import load_dotenv
import os

load_dotenv()


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

def get_emprestimos() -> dict | bool:
    db = None
    try:
        db = get_connection()
        cursor = db.cursor()
        sql = 'SELECT * FROM emprestimos'
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as erro:
        print('Erro:',erro)
        return False
    finally:
        if db is not None:
            db.close()

def insert_emprestimos(emprestimo) -> bool:
    db = None
    try:
        db = get_connection()
        sql = "INSERT INTO emprestimos (id_livro, nome_pessoa, data_emprestimo, data_devolução, valor) " \
        "VALUES (%s, %s, %s, %s, %s)"
        cursor = db.cursor()
        cursor.execute(sql, (
            emprestimo.id_livro,
            emprestimo.nome_pessoa,
            emprestimo.data_emprestimo,
            emprestimo.data_devolução,
            emprestimo.valor
        ))
        db.commit()
        return True
    except Exception as err:
        print('Erro:',err)
    finally:
        if db is not None:
            db.close()