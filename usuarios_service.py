from db import get_conn


def crear_usuario(nombre, apellido, correo, salario_base, estado, creado_por):
    con = get_conn()
    cur = con.cursor()

    cur.execute("""
        EXECUTE PROCEDURE SP_USUARIO_INSERT(
            ?, ?, ?, ?, ?, ?
        )
    """, (
        nombre,
        apellido,
        correo,
        salario_base,
        estado,
        creado_por
    ))

    con.commit()
    cur.close()
    con.close()


def obtener_usuario_por_id(id_usuario):
    con = get_conn()
    cur = con.cursor()

    cur.execute("""
        SELECT *
        FROM SP_USUARIO_GET(?)
    """, (id_usuario,))

    fila = cur.fetchone()

    cur.close()
    con.close()
    return fila


def listar_usuarios():
    con = get_conn()
    cur = con.cursor()

    cur.execute("""
        SELECT
            ID_USUARIO,
            NOMBRE,
            APELLIDO,
            CORREO_ELECTRONICO,
            SALARIO_MENSUAL_BASE,
            ESTADO
        FROM USUARIO
        ORDER BY ID_USUARIO
    """)

    filas = cur.fetchall()

    cur.close()
    con.close()
    return filas


def eliminar_usuario(id_usuario, modificado_por):
    con = get_conn()
    cur = con.cursor()

    cur.execute("""
        EXECUTE PROCEDURE SP_USUARIO_DELETE(
            ?, ?
        )
    """, (
        id_usuario,
        modificado_por
    ))

    con.commit()
    cur.close()
    con.close()
