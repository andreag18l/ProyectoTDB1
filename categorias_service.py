from db import get_conn

def crear_categoria(nombre):
    con = get_conn()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO categoria (nombre) VALUES (?)",
        (nombre,)
    )
    con.commit()
    con.close()
