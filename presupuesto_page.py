from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QFormLayout,
    QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from presupuesto_service import crear_presupuesto, listar_presupuestos

BTN_GRAY = """
QPushButton {
    background-color: #f0f0f0;
    border-radius: 8px;
    padding: 8px;
}
"""

INPUT_STYLE = """
QLineEdit {
    padding: 6px;
    border-radius: 6px;
    border: 1px solid #cfcfcf;
}
"""

class PresupuestoPage(QWidget):
    def __init__(self, app_window):
        super().__init__()
        self.app_window = app_window

        title = QLabel("Gestión de Presupuestos")
        title.setFont(QFont("Arial", 18))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Formulario
        form = QFormLayout()
        self.nombre = QLineEdit(); self.nombre.setStyleSheet(INPUT_STYLE)
        self.ano_i = QLineEdit(); self.ano_i.setStyleSheet(INPUT_STYLE)
        self.mes_i = QLineEdit(); self.mes_i.setStyleSheet(INPUT_STYLE)
        self.ano_f = QLineEdit(); self.ano_f.setStyleSheet(INPUT_STYLE)
        self.mes_f = QLineEdit(); self.mes_f.setStyleSheet(INPUT_STYLE)
        self.ingresos = QLineEdit(); self.ingresos.setStyleSheet(INPUT_STYLE)
        self.gastos = QLineEdit(); self.gastos.setStyleSheet(INPUT_STYLE)
        self.ahorro = QLineEdit(); self.ahorro.setStyleSheet(INPUT_STYLE)

        form.addRow("Nombre:", self.nombre)
        form.addRow("Año Inicio:", self.ano_i)
        form.addRow("Mes Inicio:", self.mes_i)
        form.addRow("Año Fin:", self.ano_f)
        form.addRow("Mes Fin:", self.mes_f)
        form.addRow("Ingresos:", self.ingresos)
        form.addRow("Gastos:", self.gastos)
        form.addRow("Ahorro:", self.ahorro)

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
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Periodo", "Totales"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # Layout principal
        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addLayout(form)
        layout.addWidget(self.table)
        self.setLayout(layout)

        # Cargar datos iniciales
        self.cargar()

    def guardar(self):
         try:
           id_usuario = self.app_window.usuario_activo[0]  # columna 0 = ID_USUARIO
           crear_presupuesto(
               id_usuario,
               self.nombre.text(),
               int(self.ano_i.text()),
               int(self.mes_i.text()),
               int(self.ano_f.text()),
               int(self.mes_f.text()),
               float(self.ingresos.text()),
               float(self.gastos.text()),
               float(self.ahorro.text()),
               "ACTIVO",
                "frontend"
           )
           QMessageBox.information(self, "OK", "Presupuesto creado correctamente.")
           self.cargar()
         except Exception as e:
           QMessageBox.critical(self, "Error", f"No se pudo crear el presupuesto:\n{e}")


    def cargar(self):
        self.table.setRowCount(0)
        try:
            for p in listar_presupuestos():
                row = self.table.rowCount()
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(str(p[0])))  # ID
                self.table.setItem(row, 1, QTableWidgetItem(p[2]))       # Nombre
                self.table.setItem(row, 2, QTableWidgetItem(f"{p[3]}/{p[4]} - {p[5]}/{p[6]}"))  # Periodo
                self.table.setItem(row, 3, QTableWidgetItem(
                    f"I:{p[7]} G:{p[8]} A:{p[9]}"  # Totales ingresos/gastos/ahorro
                ))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudieron cargar los presupuestos:\n{e}")
