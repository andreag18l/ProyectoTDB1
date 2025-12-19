from db import get_conn

def crear_presupuesto(id_usuario, nombre, ano_inicio, mes_inicio, ano_fin, mes_fin,
                      ingresos, gastos, ahorro, estado, creado_por):
    con = get_conn()
    cur = con.cursor()

    cur.execute("""
        EXECUTE PROCEDURE SP_PRESUPUESTO_INSERT(
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
    """, (
        id_usuario,
        nombre,
        ano_inicio,
        mes_inicio,
        ano_fin,
        mes_fin,
        ingresos,
        gastos,
        ahorro,
        estado,
        creado_por
    ))

    id_generado = cur.fetchone()[0]
    con.commit()
    cur.close()
    con.close()
    return id_generado


def listar_presupuestos():
    con = get_conn()
    cur = con.cursor()

    cur.execute("""
        SELECT *
        FROM SP_PRESUPUESTO_LIST
        ORDER BY ID_PRES
    """)

    filas = cur.fetchall()
    cur.close()
    con.close()
    return filas


def obtener_presupuesto_por_id(id_presupuesto):
    con = get_conn()
    cur = con.cursor()

    cur.execute("""
        SELECT *
        FROM SP_PRESUPUESTO_GET(?)
    """, (id_presupuesto,))

    fila = cur.fetchone()
    cur.close()
    con.close()
    return fila


def actualizar_presupuesto(id_presupuesto, ingresos, gastos, ahorro, estado, modificado_por):
    con = get_conn()
    cur = con.cursor()

    cur.execute("""
        EXECUTE PROCEDURE SP_PRESUPUESTO_UPDATE(
            ?, ?, ?, ?, ?, ?
        )
    """, (
        id_presupuesto,
        ingresos,
        gastos,
        ahorro,
        estado,
        modificado_por
    ))

    con.commit()
    cur.close()
    con.close()


def eliminar_presupuesto(id_presupuesto):
    con = get_conn()
    cur = con.cursor()

    cur.execute("""
        EXECUTE PROCEDURE SP_PRESUPUESTO_DELETE(?)
    """, (id_presupuesto,))

    con.commit()
    cur.close()
    con.close()
