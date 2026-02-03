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

