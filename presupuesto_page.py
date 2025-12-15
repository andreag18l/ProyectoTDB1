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

        btn_guardar = QPushButton("Guardar")
        btn_guardar.setStyleSheet(BTN_GRAY)
        btn_guardar.clicked.connect(self.guardar)

        btn_atras = QPushButton("Atrás")
        btn_atras.setStyleSheet(BTN_GRAY)
        btn_atras.clicked.connect(lambda: self.app_window.show_page("menu"))

        h = QHBoxLayout()
        h.addWidget(btn_atras)
        h.addWidget(btn_guardar)
        form.addRow(h)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Periodo", "Totales"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addLayout(form)
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.cargar()

    def guardar(self):
        crear_presupuesto(
            1,
            self.nombre.text(),
            int(self.ano_i.text()),
            int(self.mes_i.text()),
            int(self.ano_f.text()),
            int(self.mes_f.text()),
            float(self.ingresos.text()),
            float(self.gastos.text()),
            float(self.ahorro.text()),
            "frontend"
        )

        QMessageBox.information(self, "OK", "Presupuesto creado.")
        self.cargar()

    def cargar(self):
        self.table.setRowCount(0)
        for p in listar_presupuestos():
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(p[0])))
            self.table.setItem(row, 1, QTableWidgetItem(p[1]))
            self.table.setItem(row, 2, QTableWidgetItem(f"{p[2]}/{p[3]} - {p[4]}/{p[5]}"))
            self.table.setItem(row, 3, QTableWidgetItem(
                f"I:{p[6]} G:{p[7]} A:{p[8]}"
            ))
