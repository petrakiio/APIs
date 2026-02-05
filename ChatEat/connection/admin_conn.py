from .core import get_connection


def users_get():
    db = None
    try:
        db = get_connection()
        cursor = db.cursor()
        sql = 'SELECT * FROM clientes'
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as err:
        print('Erro:', err)
        return None
    finally:
        if db is not None:
            db.close()


def users_del(id):
    db = None
    try:
        db = get_connection()
        cursor = db.cursor()
        sql = 'DELETE FROM clientes WHERE id = %s'
        cursor.execute(sql, (id,))
        db.commit()
        return True
    except Exception as err:
        print('Erro:', err)
        return False
    finally:
        if db is not None:
            db.close()


def users_admin(id):
    db = None
    try:
        db = get_connection()
        cursor = db.cursor()
        sql = 'UPDATE clientes SET is_admin = 1 WHERE id = %s'
        cursor.execute(sql, (id,))
        db.commit()
        return True
    except Exception as err:
        print('Erro:', err)
        return False
    finally:
        if db is not None:
            db.close()


def users_rm_admin(id):
    db = None
    try:
        db = get_connection()
        cursor = db.cursor()
        sql = 'UPDATE clientes SET is_admin = 0 WHERE id = %s'
        cursor.execute(sql, (id,))
        db.commit()
        return True
    except Exception as e:
        print('Erro:', e)
        return False
    finally:
        if db is not None:
            db.close()
