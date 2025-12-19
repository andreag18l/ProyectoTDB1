from PyQt6.QtWidgets import (
    QWidget, QComboBox, QDateEdit, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QFormLayout,
    QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QDate
from datetime import date

from transacciones_service import crear_transaccion, listar_transacciones
from presupuesto_service import listar_presupuestos

BTN_GRAY = """
QPushButton {
    background-color: #f0f0f0;
    border-radius: 8px;
    padding: 8px;
}
"""

INPUT_STYLE = """
QLineEdit,QComboBox,QDateEdit{
    padding: 6px;
    border-radius: 6px;
    border: 1px solid #cfcfcf;
}
"""

class TransaccionesPage(QWidget):
    def __init__(self, app_window):
        super().__init__()
        self.app_window = app_window
        # Título
        title = QLabel("Gestión de Transacciones")
        title.setFont(QFont("Arial", 18))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Formulario
        form = QFormLayout()
        self.descripcion = QLineEdit(); self.descripcion.setStyleSheet(INPUT_STYLE)
        self.monto = QLineEdit(); self.monto.setStyleSheet(INPUT_STYLE)
        self.tipo = QComboBox(); self.tipo.addItems(["INGRESO", "GASTO", "AHORRO"]); self.tipo.setStyleSheet(INPUT_STYLE)
        self.fecha = QDateEdit(); self.fecha.setDate(QDate.currentDate()); self.fecha.setCalendarPopup(True); self.fecha.setStyleSheet(INPUT_STYLE)
        self.ano = QLineEdit(); self.ano.setStyleSheet(INPUT_STYLE)
        self.mes = QLineEdit(); self.mes.setStyleSheet(INPUT_STYLE)
        self.presupuesto = QComboBox(); self.presupuesto.setStyleSheet(INPUT_STYLE)

        form.addRow("Descripción:", self.descripcion)
        form.addRow("Monto:", self.monto)
        form.addRow("Tipo:", self.tipo)
        form.addRow("Fecha real:", self.fecha)
        form.addRow("Año imputación:", self.ano)
        form.addRow("Mes imputación:", self.mes)
        form.addRow("Presupuesto:", self.presupuesto)

        # Botones
        btn_guardar = QPushButton("Guardar")
        btn_guardar.setStyleSheet(BTN_GRAY)
        btn_guardar.clicked.connect(self.guardar)

        btn_atras = QPushButton("Atrás")
        btn_atras.setStyleSheet(BTN_GRAY)
        btn_atras.clicked.connect(lambda: self.app_window.show_page("dashboard"))

        h = QHBoxLayout()
        h.addWidget(btn_atras)
        h.addWidget(btn_guardar)
        form.addRow(h)

        # Tabla
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["ID", "Descripción", "Monto", "Fecha", "Tipo"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # Layout principal
        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addLayout(form)
        layout.addWidget(self.table)
        self.setLayout(layout)

        # Cargar presupuestos y transacciones
        self.cargar_presupuestos()
        self.cargar()

    def cargar_presupuestos(self):
        """Carga todos los presupuestos en el ComboBox"""
        self.presupuesto.clear()
        for p in listar_presupuestos():  # sin filtrar por usuario, igual que antes
            self.presupuesto.addItem(f"{p[2]} (ID:{p[0]})", p[0])

    def guardar(self):
        try:
            if not hasattr(self.app_window, "usuario_activo") or not self.app_window.usuario_activo:
                QMessageBox.warning(self, "Error", "No hay usuario activo.")
                return

            id_usuario = self.app_window.usuario_activo[0]  # toma el usuario activo
            id_presupuesto = self.presupuesto.currentData()
            ano = int(self.ano.text())
            mes = int(self.mes.text())

            # Por ahora subcategoría fija porque aún no hay subcategorías
            crear_transaccion(
                id_usuario=id_usuario,
                id_presupuesto=id_presupuesto,
                id_subcategoria=3,
                id_obligacion=None,
                tipo=self.tipo.currentText(),
                ano=ano,
                mes=mes,
                descripcion=self.descripcion.text(),
                monto=float(self.monto.text()),
                fecha=self.fecha.date().toPyDate(),
                metodo_pago="Efectivo",
                num_factura="",
                observaciones="",
                creado_por="frontend"
            )

            QMessageBox.information(self, "OK", "Transacción creada correctamente.")
            self.cargar()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo crear la transacción:\n{e}")

    def cargar(self):
        """Carga las transacciones en la tabla"""
        self.table.setRowCount(0)
        try:
            if not hasattr(self.app_window, "usuario_activo") or not self.app_window.usuario_activo:
                return

            id_usuario = self.app_window.usuario_activo[0]
            for t in listar_transacciones(id_usuario):
                row = self.table.rowCount()
                self.table.insertRow(row)
                # indices según SP_TRANSACCION_LIST: ID_TRANS, SUBCAT, PRES, TIPO, MONTO, FECHA, DESCRI
                self.table.setItem(row, 0, QTableWidgetItem(str(t[0])))  # ID_TRANS
                self.table.setItem(row, 1, QTableWidgetItem(t[6]))       # DESCRIPCION
                self.table.setItem(row, 2, QTableWidgetItem(str(t[4])))  # MONTO
                self.table.setItem(row, 3, QTableWidgetItem(str(t[5])))  # FECHA
                self.table.setItem(row, 4, QTableWidgetItem(t[3]))       # TIPO

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar las transacciones:\n{e}")
