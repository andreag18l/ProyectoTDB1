# transacciones_service.py
from db import get_conn

def crear_transaccion(
    id_usuario,
    id_presupuesto,
    id_subcategoria,
    id_obligacion,
    tipo,
    ano,
    mes,
    descripcion,
    monto,
    fecha,
    metodo_pago,
    num_factura,
    observaciones,
    creado_por
):
    """
    Crea una transacción en la base de datos usando el SP_TRANSACCION_INSERT.
    """
    con = get_conn()
    cur = con.cursor()

    cur.execute("""
        EXECUTE PROCEDURE SP_TRANSACCION_INSERT(
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
    """, (
        id_usuario,
        id_presupuesto,
        id_subcategoria,
        id_obligacion,
        tipo,
        ano,
        mes,
        descripcion,
        monto,
        fecha,
        metodo_pago,
        num_factura,
        observaciones,
        creado_por
    ))

    con.commit()
    cur.close()
    con.close()


def listar_transacciones(id_usuario):
    """
    Devuelve todas las transacciones de un usuario.
    """
    con = get_conn()
    cur = con.cursor()

    cur.execute("""
        SELECT *
        FROM SP_TRANSACCION_LIST(?)
    """, (id_usuario,))

    filas = cur.fetchall()
    cur.close()
    con.close()

    # filas: cada elemento es (ID_TRANS, SUBCAT, PRES, TIPO, MONTO, FECHA, DESCRI)
    return filas


def obtener_transaccion(id_transaccion):
    """
    Obtiene una transacción específica por su ID usando SP_TRANSACCION_GET.
    """
    con = get_conn()
    cur = con.cursor()

    cur.execute("""
        SELECT *
        FROM SP_TRANSACCION_GET(?)
    """, (id_transaccion,))

    fila = cur.fetchone()
    cur.close()
    con.close()
    return fila


def actualizar_transaccion(
    id_transaccion,
    descripcion,
    monto,
    fecha,
    metodo_pago,
    observaciones,
    modificado_por
):
    """
    Actualiza los datos de una transacción existente.
    """
    con = get_conn()
    cur = con.cursor()

    cur.execute("""
        EXECUTE PROCEDURE SP_TRANSACCION_UPDATE(
            ?, ?, ?, ?, ?, ?
        )
    """, (
        id_transaccion,
        descripcion,
        monto,
        fecha,
        metodo_pago,
        observaciones,
        modificado_por
    ))

    con.commit()
    cur.close()
    con.close()
