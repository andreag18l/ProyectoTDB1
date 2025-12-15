from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QFormLayout, QMessageBox, QTableWidget, QTableWidgetItem,
    QComboBox, QHeaderView, QGroupBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from categorias_service import crear_categoria, listar_categorias


BTN_GRAY = """
QPushButton {
    background-color: #f0f0f0;
    border: 1px solid #d0d0d0;
    border-radius: 8px;
    padding: 8px;
    font-size: 14px;
}
"""

INPUT_STYLE = """
QLineEdit, QComboBox {
    padding: 6px;
    border-radius: 6px;
    border: 1px solid #cfcfcf;
}
"""

WINDOW_BG = "background-color: #ffffff;"
TITLE_STYLE = "font-size: 20px; font-weight: bold;"


class CategoriasPage(QWidget):
    def __init__(self, app_window):
        super().__init__()
        self.app_window = app_window
        self.setStyleSheet(WINDOW_BG)

        title = QLabel("Gestión de Categorías")
        title.setFont(QFont("Arial", 18))
        title.setStyleSheet(TITLE_STYLE)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        form = QFormLayout()

        self.nombre = QLineEdit()
        self.nombre.setStyleSheet(INPUT_STYLE)

        self.tipo = QComboBox()
        self.tipo.addItems(["Ingreso", "Gasto", "Ahorro"])
        self.tipo.setStyleSheet(INPUT_STYLE)

        form.addRow("Nombre:", self.nombre)
        form.addRow("Tipo:", self.tipo)

        btn_guardar = QPushButton("Guardar")
        btn_guardar.setStyleSheet(BTN_GRAY)
        btn_guardar.clicked.connect(self.guardar_categoria)

        btn_atras = QPushButton("Atrás")
        btn_atras.setStyleSheet(BTN_GRAY)
        btn_atras.clicked.connect(lambda: self.app_window.show_page("menu"))

        h = QHBoxLayout()
        h.addWidget(btn_atras)
        h.addWidget(btn_guardar)

        form.addRow(h)

        group = QGroupBox("Crear Categoría")
        group.setLayout(form)

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Tipo"])
        self.table.setColumnHidden(0, True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(group)
        layout.addWidget(QLabel("Lista de Categorías"))
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.cargar_categorias()

    def guardar_categoria(self):
        if not self.nombre.text().strip():
            QMessageBox.warning(self, "Validación", "Ingrese el nombre.")
            return

        crear_categoria(
            self.nombre.text(),
            None,
            self.tipo.currentText(),
            None,
            None,
            1,
            "frontend"
        )

        QMessageBox.information(self, "OK", "Categoría creada.")
        self.nombre.clear()
        self.cargar_categorias()

    def cargar_categorias(self):
        self.table.setRowCount(0)
        for c in listar_categorias():
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(c[0])))
            self.table.setItem(row, 1, QTableWidgetItem(c[1]))
            self.table.setItem(row, 2, QTableWidgetItem(c[2]))
