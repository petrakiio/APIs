from .core import get_connection


def get_entregador():
    db = None
    try:
        db = get_connection()
        cursor = db.cursor()
        sql = "SELECT * FROM entregadores"
        cursor.execute(sql)
        resultado = cursor.fetchall()
        if resultado is not None:
            return resultado
        return []
    except Exception as err:
        print("Erro:", err)
        return False
    finally:
        if db is not None:
            db.close()


def add_entregador(entregador: object):
    db = None
    try:
        db = get_connection()
        cursor = db.cursor()
        sql = (
            "INSERT INTO entregadores(nome,usuario,email,telefone,veiculo,placa,ativo) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s)"
        )
        cursor.execute(
            sql,
            (
                entregador.nome,
                entregador.usuario,
                entregador.email,
                entregador.telefone,
                entregador.veiculo,
                entregador.placa,
                entregador.ativo,
            ),
        )
        db.commit()
        return True
    except Exception as err:
        print("Erro:", err)
        return False
    finally:
        if db is not None:
            db.close()


def rm_entregador(nome: str):
    db = None
    try:
        db = get_connection()
        cursor = db.cursor()
        sql = "DELETE FROM entregadores WHERE nome = %s LIMIT 1"
        cursor.execute(sql, (nome,))
        db.commit()
        return cursor.rowcount > 0
    except Exception as err:
        print("Erro:", err)
        return False
    finally:
        if db is not None:
            db.close()
