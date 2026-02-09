from connection.core import get_connection

def inserir_feedback(feed) -> bool:
    db = None
    try:
        db = get_connection()
        cursor = db.cursor()
        sql = "INSERT INTO feed_valeler(nome, gmail, mensagem) VALUES (%s, %s, %s)"
        cursor.execute(sql, (feed.nome, feed.gmail, feed.mensagem))
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

def get_all_feedbacks():
    db = None
    try:
        db = get_connection()
        cursor = db.cursor()
        sql = "SELECT * FROM feed_valeler"
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as err:
        print('Erro:', err)
        return []
    finally:
        if db is not None:
            db.close()
    
def deletar_feedback(id) -> bool:
    db = None
    try:
        db = get_connection()
        cursor = db.cursor()
        sql = "DELETE FROM feed_valeler WHERE id_feedback = %s"
        cursor.execute(sql, (id,))
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