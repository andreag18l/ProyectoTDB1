from db import get_conn

# -----------------------------------------
# Crear categoría
# -----------------------------------------
def crear_categoria(
    nombre_categoria,
    descripcion,
    tipo,
    icono,
    color,
    orden,
    creado_por
):
    con = get_conn()
    cur = con.cursor()

    cur.execute("""
        EXECUTE PROCEDURE SP_CATEGORIA_INSERT(
            ?, ?, ?, ?, ?, ?, ?
        )
    """, (
        nombre_categoria,
        descripcion,
        tipo,
        icono,
        color,
        orden,
        creado_por
    ))

    con.commit()
    cur.close()
    con.close()


# -----------------------------------------
# Listar categorías
# -----------------------------------------
def listar_categorias():
    con = get_conn()
    cur = con.cursor()

    cur.execute("""
        SELECT
            ID_CATEGORIA,
            NOMBRE_CATEGORIA,
            DESCRIPCION,
            TIPO,
            ICONO,
            COLOR,
            ORDEN_PRESENTACION
        FROM CATEGORIA
        ORDER BY ORDEN_PRESENTACION
    """)

    filas = cur.fetchall()
    cur.close()
    con.close()

    return filas
