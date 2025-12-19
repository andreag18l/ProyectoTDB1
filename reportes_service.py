from db import get_conn
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
import matplotlib.pyplot as plt
import numpy as np

# -----------------------------
# REPORTE 1: RESUMEN MENSUAL
# -----------------------------
def reporte_resumen_mensual(id_usuario):
    """
    Genera PDF con gráfico de barras y tabla resumen mensual
    """
    con = get_conn()
    cur = con.cursor()

    cur.execute("""
        SELECT ano, mes,
            SUM(CASE WHEN tipo='INGRESO' THEN monto ELSE 0 END) AS ingresos,
            SUM(CASE WHEN tipo='GASTO' THEN monto ELSE 0 END) AS gastos,
            SUM(CASE WHEN tipo='AHORRO' THEN monto ELSE 0 END) AS ahorro
        FROM transaccion
        WHERE id_usuario = ?
        GROUP BY ano, mes
        ORDER BY ano, mes
    """, (id_usuario,))

    resultados = cur.fetchall()
    con.close()

    if not resultados:
        raise Exception("No hay transacciones para este usuario.")

    # Preparar gráfico
    meses = [f"{r[1]}/{r[0]}" for r in resultados]
    ingresos = [float(r[2]) for r in resultados]
    gastos = [float(r[3]) for r in resultados]
    ahorros = [float(r[4]) for r in resultados]

    x = np.arange(len(meses))
    width = 0.25

    plt.figure(figsize=(10,5))
    plt.bar(x - width, ingresos, width, label='Ingresos', color='green')
    plt.bar(x, gastos, width, label='Gastos', color='red')
    plt.bar(x + width, ahorros, width, label='Ahorro', color='blue')
    plt.xticks(x, meses, rotation=45)
    plt.ylabel("Monto")
    plt.title("Resumen Mensual de Ingresos, Gastos y Ahorro")
    plt.legend()
    plt.tight_layout()
    plt.savefig("reporte_resumen_mensual.png")
    plt.close()

    # Generar PDF
    c = canvas.Canvas("reporte_resumen_mensual.pdf", pagesize=letter)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 750, "Reporte 1: Resumen Mensual de Ingresos, Gastos y Ahorros")

    # Dibujar gráfico arriba
    c.drawImage("reporte_resumen_mensual.png", 50, 450, width=500, height=250)

    # Tabla debajo del gráfico
    datos_tabla = [["Mes/Año","Ingresos","Gastos","Ahorro","Balance"]]
    for r in resultados:
        balance = float(r[2]) - float(r[3]) - float(r[4])
        datos_tabla.append([
            f"{r[1]}/{r[0]}", 
            f"L {r[2]:,.2f}", 
            f"L {r[3]:,.2f}", 
            f"L {r[4]:,.2f}", 
            f"L {balance:,.2f}"
        ])

    tabla = Table(datos_tabla, colWidths=[100,100,100,100,100])
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('ALIGN',(1,1),(-1,-1),'RIGHT')
    ]))
    tabla.wrapOn(c, 50, 50)
    tabla.drawOn(c, 50, 50)

    c.save()
    return True, "Reporte 1 generado correctamente: reporte_resumen_mensual.pdf"

# -----------------------------
# REPORTE 2: DISTRIBUCIÓN DE GASTOS POR CATEGORÍA
# -----------------------------
def reporte_gastos_por_descripcion(id_usuario):
    """
    Genera PDF con la distribución de gastos por categoría
    """
    try:
        con = get_conn()
        cur = con.cursor()

        # Obtener totales por categoría usando INNER JOIN
        cur.execute("""
            SELECT C.ID_CATEGORIA, C.NOMBRE, SUM(T.MONTO) AS TOTAL_GASTOS, COUNT(T.ID_TRANSACCION) AS NUM_TRANS
            FROM TRANSACCION T
            INNER JOIN SUBCATEGORIA S ON T.ID_SUBCATEGORIA = S.ID_SUBCATEGORIA
            INNER JOIN CATEGORIA C ON S.ID_CATEGORIA = C.ID_CATEGORIA
            WHERE T.ID_USUARIO = ? AND T.TIPO='GASTO'
            GROUP BY C.ID_CATEGORIA, C.NOMBRE
            ORDER BY TOTAL_GASTOS DESC
        """, (id_usuario,))

        data = cur.fetchall()
        con.close()

        if not data:
            raise Exception("No hay gastos registrados para este usuario.")

        # Preparar gráfico de pastel
        nombres = [r[1] for r in data]
        totales = [float(r[2]) for r in data]

        plt.figure(figsize=(6,6))
        plt.pie(totales, labels=nombres, autopct='%1.1f%%', startangle=90)
        plt.title("Distribución de Gastos por Categoría")
        plt.tight_layout()
        plt.savefig("reporte_gastos_categoria.png")
        plt.close()

        # Generar PDF
        c = canvas.Canvas("reporte_gastos_categoria.pdf", pagesize=letter)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, 750, "Reporte 2: Distribución de Gastos por Categoría")

        # Dibujar gráfico arriba
        c.drawImage("reporte_gastos_categoria.png", 100, 400, width=400, height=300)

        # Tabla debajo del gráfico
        y = 380
        datos_tabla = [["Categoría", "Total Gastos", "Nº Transacciones"]]
        total_general = 0
        for r in data:
            nombre = r[1]
            total = float(r[2])
            num = r[3]
            datos_tabla.append([nombre, f"L {total:,.2f}", str(num)])
            total_general += total

        tabla = Table(datos_tabla, colWidths=[200,150,150])
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('ALIGN',(1,1),(-1,-1),'RIGHT')
        ]))
        tabla.wrapOn(c, 50, 50)
        tabla.drawOn(c, 50, 50)

        # Total general debajo
        c.drawString(50, 20, f"Total General Gastos: L {total_general:,.2f}")

        c.save()
        return True, "Reporte 2 generado correctamente: reporte_gastos_categoria.pdf"

    except Exception as e:
        return False, f"No se pudo generar el Reporte 2:\n{e}"
