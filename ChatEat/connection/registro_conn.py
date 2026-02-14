from .core import get_connection

def add_motivo(motivo:object):
    db = None
    try:
        db = get_connection()
        cursor = db.cursor()
        sql = 'INSERT registro(nome,motivo,observacao) VALUES (%s,%s,%s)'
        cursor.execute(sql,(motivo.nome,motivo.mt,motivo.obs))
        db.commit()
        return True
    except Exception as err:
        print('Erro:',err)
    finally:
        if db is not None:
            db.close()

