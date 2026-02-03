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

def insert_books() -> bool:
    db = None
    try:
        db = get_connection()
        sql = "INSERT INTO livros (titulo, autor, editora, ano_publicacao, isbn, categoria, total_unidades, unidades_disponiveis) " \
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor = db.cursor()
