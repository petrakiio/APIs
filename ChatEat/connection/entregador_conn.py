from .core import get_connection

def get_entregador():
    db = None
    try:
        db = get_connection()
        cursor = db.cursor()
        sql = 'SELECT * FROM clientes WHERE is_motoboy = %s'
        cursor.execute(sql,(True))
        resultado = cursor.fetchall()
        if resultado is not None:
            return resultado
    except Exception as err:
        print('Erro:',err)
        return False
    finally:
        if db is not None:
            db.close