# transacciones_page.py
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QFormLayout, QMessageBox, QTableWidget, QTableWidgetItem, QComboBox,
    QSpinBox, QHeaderView, QGroupBox, QDateEdit
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QDate
from datetime import datetime

BTN_GRAY = """
    QPushButton {
        background-color: #f0f0f0;
        border: 1px solid #d0d0d0;
        border-radius: 8px;
        padding: 8px 10px;
        font-size: 14px;
        color: #222222;
    }
    QPushButton:hover {
        background-color: #e6e6e6;
    }
"""

BTN_DANGER = """
    QPushButton {
        background-color: #b91c1c;
        color: white;
        border-radius: 8px;
        padding: 8px 10px;
        font-size: 14px;
    }
    QPushButton:hover {
        background-color: #991616;
    }
"""

INPUT_STYLE = """
    QLineEdit, QComboBox, QSpinBox, QDateEdit {
        padding: 6px;
        border-radius: 6px;
        border: 1px solid #cfcfcf;
        font-size: 14px;
    }
"""

WINDOW_BG = "background-color: #ffffff; color: #222222; font-family: Arial;"
TITLE_STYLE = "font-size: 20px; font-weight: bold; color: #2b2b2b;"

# Lista de transacciones (temporal, luego DB)
transacciones = []

class TransaccionesPage(QWidget):
    def __init__(self, app_window):
        super().__init__()
        self.app_window = app_window
        self.setStyleSheet(WINDOW_BG)
        self.editing_id = None

        # ------------------------------
        # Título
        # ------------------------------
        title = QLabel("Gestión de Transacciones")
        title.setStyleSheet(TITLE_STYLE)
        title.setFont(QFont("Arial", 18))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ------------------------------
        # Formulario
        # ------------------------------
        form_group = QGroupBox("Crear / Editar Transacción")
        form_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        form_layout = QFormLayout()

        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setDisplayFormat("dd/MM/yyyy")
        self.date_edit.setStyleSheet(INPUT_STYLE)

        self.input_concepto = QLineEdit()
        self.input_concepto.setFixedWidth(320)
        self.input_concepto.setStyleSheet(INPUT_STYLE)

        self.combo_categoria = QComboBox()
        self.combo_categoria.addItems(["Ingreso", "Gasto", "Ahorro"])
        self.combo_categoria.setFixedWidth(200)

        self.input_monto = QLineEdit()
        self.input_monto.setFixedWidth(200)
        self.input_monto.setStyleSheet(INPUT_STYLE)
        self.input_monto.setPlaceholderText("0.00")

        form_layout.addRow("Fecha:", self.date_edit)
        form_layout.addRow("Concepto:", self.input_concepto)
        form_layout.addRow("Categoría:", self.combo_categoria)
        form_layout.addRow("Monto:", self.input_monto)

        # Botones
        btn_guardar = QPushButton("Guardar"); btn_guardar.setStyleSheet(BTN_GRAY); btn_guardar.clicked.connect(self.guardar_transaccion)
        btn_limpiar = QPushButton("Limpiar"); btn_limpiar.setStyleSheet(BTN_GRAY); btn_limpiar.clicked.connect(self.limpiar_form)
        btn_atras = QPushButton("Atrás"); btn_atras.setStyleSheet(BTN_GRAY); btn_atras.clicked.connect(lambda: self.app_window.show_page("menu"))

        h_buttons = QHBoxLayout()
        h_buttons.addWidget(btn_atras)
        h_buttons.addWidget(btn_limpiar)
        h_buttons.addWidget(btn_guardar)

        form_layout.addRow(h_buttons)
        form_group.setLayout(form_layout)

        # ------------------------------
        # Tabla
        # ------------------------------
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(["ID","Fecha","Concepto","Categoría","Monto","Acciones"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setColumnHidden(0, True)
        self.table.setEditTriggers(self.table.EditTrigger.NoEditTriggers)

        # ------------------------------
        # Layout global
        # ------------------------------
        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(form_group)
        layout.addWidget(QLabel("Lista de Transacciones:"))
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.actualizar_tabla()

    # =====================================================
    # Validación
    # =====================================================
    def validar_form(self):
        if not self.input_concepto.text().strip():
            QMessageBox.warning(self, "Validación", "Debes ingresar un concepto.")
            return False
        try:
            monto = float(self.input_monto.text() or "0")
            if monto <= 0:
                raise ValueError
        except:
            QMessageBox.warning(self, "Validación", "Monto inválido o <= 0.")
            return False
        return True

    # =====================================================
    # Guardar transacción
    # =====================================================
    def guardar_transaccion(self):
        if not self.validar_form():
            return

        fecha = self.date_edit.date().toPyDate()
        concepto = self.input_concepto.text().strip()
        categoria = self.combo_categoria.currentText()
        monto = float(self.input_monto.text())

        global transacciones
        if self.editing_id is None:
            nuevo = {
                "id": str(int(datetime.now().timestamp()*1000)),
                "fecha": fecha,
                "concepto": concepto,
                "categoria": categoria,
                "monto": monto
            }
            transacciones.append(nuevo)
            QMessageBox.information(self, "Transacción", "Transacción creada.")
        else:
            for t in transacciones:
                if t["id"] == self.editing_id:
                    t.update({
                        "fecha": fecha,
                        "concepto": concepto,
                        "categoria": categoria,
                        "monto": monto
                    })
            QMessageBox.information(self, "Transacción", "Transacción actualizada.")
            self.editing_id = None

        self.limpiar_form()
        self.actualizar_tabla()

    # =====================================================
    # Limpiar formulario
    # =====================================================
    def limpiar_form(self):
        self.input_concepto.clear()
        self.input_monto.clear()
        self.date_edit.setDate(QDate.currentDate())
        self.combo_categoria.setCurrentIndex(0)
        self.editing_id = None

    # =====================================================
    # Tabla
    # =====================================================
    def actualizar_tabla(self):
        self.table.setRowCount(0)
        for t in transacciones:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(t["id"]))
            self.table.setItem(row, 1, QTableWidgetItem(t["fecha"].strftime("%d/%m/%Y")))
            self.table.setItem(row, 2, QTableWidgetItem(t["concepto"]))
            self.table.setItem(row, 3, QTableWidgetItem(t["categoria"]))
            self.table.setItem(row, 4, QTableWidgetItem(f"{t['monto']:.2f}"))

            # botones editar/eliminar
            btn_edit = QPushButton("Editar"); btn_edit.setStyleSheet(BTN_GRAY)
            btn_del = QPushButton("Eliminar"); btn_del.setStyleSheet(BTN_DANGER)
            btn_edit.clicked.connect(lambda checked, tid=t["id"]: self.cargar_edicion(tid))
            btn_del.clicked.connect(lambda checked, tid=t["id"]: self.eliminar(tid))

            cont = QWidget()
            hl = QHBoxLayout()
            hl.setContentsMargins(0,0,0,0)
            hl.addWidget(btn_edit)
            hl.addWidget(btn_del)
            cont.setLayout(hl)
            self.table.setCellWidget(row, 5, cont)

    # =====================================================
    # Editar
    # =====================================================
    def cargar_edicion(self, tid):
        for t in transacciones:
            if t["id"] == tid:
                self.editing_id = tid
                self.date_edit.setDate(QDate(t["fecha"].year, t["fecha"].month, t["fecha"].day))
                self.input_concepto.setText(t["concepto"])
                self.combo_categoria.setCurrentText(t["categoria"])
                self.input_monto.setText(str(t["monto"]))
                break

    # =====================================================
    # Eliminar
    # =====================================================
    def eliminar(self, tid):
        global transacciones
        r = QMessageBox.question(self, "Eliminar", "¿Eliminar esta transacción?",
                                 QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if r == QMessageBox.StandardButton.Yes:
            transacciones = [t for t in transacciones if t["id"] != tid]
            self.actualizar_tabla()
