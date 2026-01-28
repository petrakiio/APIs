from conn import get_connection
import pymysql
from flask import jsonify

#Feedbacks methods

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

def deletar(id):
    db = None
    try:
        db = get_connection()
        cursor = db.cursor()
        sql = 'DELETE FROM feedback WHERE id = %s'
        cursor.execute(sql,(id))
        db.commit()
        return True
    except Exception as e:
        return False
    finally:
        if db not in None:
            db.close()