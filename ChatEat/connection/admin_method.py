from conn import get_connection
import pymysql
from flask import jsonify

def feeds():
    db = None
    try:
        db = get_connection()
        cursor = db.cursor()
        sql = 'SELECT * FROM feedback'
        cursor.execute(sql)
        r = cursor.fetchall()
        return jsonify(r)
    except Exception as e:
        return print('Erro:',e)
    finally:
        if db not in None:
            db.close()

feeds()