from connection.conn import get_connection
import pymysql

# Feedbacks methods
def feeds():
    db = None
    try:
        db = get_connection()
        cursor = db.cursor(pymysql.cursors.DictCursor)
        sql = 'SELECT * FROM feedback'
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print('Erro:', e)
        return []
    finally:
        if db is not None:
            db.close()


def deletar(feedback_id):
    db = None
    try:
        db = get_connection()
        cursor = db.cursor()
        sql = 'DELETE FROM feedback WHERE id = %s'
        cursor.execute(sql, (feedback_id,))
        db.commit()
        return cursor.rowcount > 0
    except Exception as e:
        print('Erro:', e)
        return False
    finally:
        if db is not None:
            db.close()
