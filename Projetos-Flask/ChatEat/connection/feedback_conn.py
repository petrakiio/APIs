from .core import get_connection


def add_com(user, comentario, nota):
    db = None
    try:
        db = get_connection()
        cursor = db.cursor()
        sql = 'INSERT INTO feedback(usuario_id, comentario, nota) VALUES (%s, %s, %s)'
        cursor.execute(sql, (user, comentario, nota))
        db.commit()
        cursor.close()
        return True
    except Exception as e:
        print(f"Erro ao inserir feedback: {e}")
        return False
    finally:
        if db:
            db.close()


def feeds():
    db = None
    try:
        db = get_connection()
        cursor = db.cursor()
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
