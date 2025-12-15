from db import get_conn

# -----------------------------------------
# Crear presupuesto
# -----------------------------------------
def crear_presupuesto(
    id_usuario,
    nombre_presupuesto,
    ano_inicio,
    mes_inicio,
    ano_fin,
    mes_fin,
    total_ingresos,
    total_gastos,
    total_ahorro,
    creado_por
):
    con = get_conn()
    cur = con.cursor()

    cur.execute("""
        EXECUTE PROCEDURE SP_PRESUPUESTO_INSERT(
            ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
    """, (
        id_usuario,
        nombre_presupuesto,
        ano_inicio,
        mes_inicio,
        ano_fin,
        mes_fin,
        total_ingresos,
        total_gastos,
        total_ahorro,
        creado_por
    ))

    con.commit()
    cur.close()
    con.close()


# -----------------------------------------
# Listar presupuestos
# -----------------------------------------
def listar_presupuestos():
    con = get_conn()
    cur = con.cursor()

    cur.execute("""
        SELECT
            ID_PRESUPUESTO,
            NOMBRE_PRESUPUESTO,
            ANO_INICIO,
            MES_INICIO,
            ANO_FIN,
            MES_FIN,
            TOTAL_INGRESOS_PLANIFICADOS,
            TOTAL_GASTOS_PLANIFICADOS,
            TOTAL_AHORRO_PLANIFICADO,
            ESTADO
        FROM PRESUPUESTO
        ORDER BY CREADO_EN DESC
    """)

    filas = cur.fetchall()
    cur.close()
    con.close()

    return filas
