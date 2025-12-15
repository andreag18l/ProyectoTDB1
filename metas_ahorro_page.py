# metas_ahorro_page.py
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QFormLayout, QMessageBox, QTableWidget, QTableWidgetItem, QComboBox,
    QSpinBox, QHeaderView, QGroupBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from datetime import datetime

# ------------------------------
# Estilos (reutilizamos)
# ------------------------------
BTN_GRAY = """
    QPushButton {
        background-color: #f0f0f0;
        border: 1px solid #d0d0d0;
        border-radius: 8px;
        padding: 6px 10px;
        font-size: 14px;
        color: #222222;
    }
    QPushButton:hover { background-color: #e6e6e6; }
"""

BTN_DANGER = """
    QPushButton {
        background-color: #b91c1c;
        color: white;
        border-radius: 8px;
        padding: 6px 10px;
        font-size: 14px;
    }
    QPushButton:hover { background-color: #991616; }
"""

INPUT_STYLE = """
    QLineEdit, QComboBox, QSpinBox {
        padding: 6px;
        border-radius: 6px;
        border: 1px solid #cfcfcf;
        font-size: 14px;
    }
"""

WINDOW_BG = "background-color: #ffffff; color: #222222; font-family: Arial;"
TITLE_STYLE = "font-size: 20px; font-weight: bold; color: #2b2b2b;"

# Lista de metas de ahorro (simulación, reemplazar con BD luego)
metas_ahorro = []

# Lista de subcategorías de ahorro (ejemplo)
subcategorias_ahorro = ["General", "Fondo Vacaciones", "Inversiones", "Emergencia"]

class MetasAhorroPage(QWidget):
    def __init__(self, app_window):
        super().__init__()
        self.app_window = app_window
        self.setStyleSheet(WINDOW_BG)
        self.editing_id = None

        # ------------------------------
        # Título
        # ------------------------------
        title = QLabel("Metas de Ahorro")
        title.setStyleSheet(TITLE_STYLE)
        title.setFont(QFont("Arial", 18))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ------------------------------
        # Formulario
        # ------------------------------
        form_group = QGroupBox("Crear / Editar Meta de Ahorro")
        form_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        form_layout = QFormLayout()

        self.input_nombre = QLineEdit(); self.input_nombre.setFixedWidth(300); self.input_nombre.setStyleSheet(INPUT_STYLE)
        self.input_monto = QLineEdit(); self.input_monto.setPlaceholderText("0.00"); self.input_monto.setFixedWidth(150); self.input_monto.setStyleSheet(INPUT_STYLE)

        self.spin_year = QSpinBox(); self.spin_year.setRange(datetime.now().year, 2100); self.spin_year.setValue(datetime.now().year)
        self.combo_month = QComboBox(); self.combo_month.addItems([str(i) for i in range(1,13)])

        self.combo_subcat = QComboBox(); self.combo_subcat.addItems(subcategorias_ahorro); self.combo_subcat.setFixedWidth(200)
        self.combo_estado = QComboBox(); self.combo_estado.addItems(["En progreso","Cumplida","Cancelada"]); self.combo_estado.setFixedWidth(150)

        form_layout.addRow("Nombre:", self.input_nombre)
        form_layout.addRow("Monto objetivo:", self.input_monto)

        h_fecha = QHBoxLayout()
        h_fecha.addWidget(QLabel("Mes:")); h_fecha.addWidget(self.combo_month)
        h_fecha.addWidget(QLabel("Año:")); h_fecha.addWidget(self.spin_year)
        form_layout.addRow("Fecha límite:", h_fecha)

        form_layout.addRow("Subcategoría:", self.combo_subcat)
        form_layout.addRow("Estado:", self.combo_estado)

        # Botones
        btn_guardar = QPushButton("Guardar"); btn_guardar.setStyleSheet(BTN_GRAY); btn_guardar.clicked.connect(self.guardar_meta)
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
        self.table = QTableWidget(0,7)
        self.table.setHorizontalHeaderLabels(["ID","Nombre","Monto","Fecha límite","Subcategoría","Estado","Acciones"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setColumnHidden(0, True)  # id oculto
        self.table.setEditTriggers(self.table.EditTrigger.NoEditTriggers)

        # ------------------------------
        # Layout global
        # ------------------------------
        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(form_group)
        layout.addWidget(QLabel("Lista de Metas de Ahorro:"))
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.actualizar_tabla()

    # ------------------------------
    # Validaciones
    # ------------------------------
    def validar_form(self):
        nombre = self.input_nombre.text().strip()
        if not nombre:
            QMessageBox.warning(self, "Validación", "Debes ingresar un nombre.")
            return False

        try:
            monto = float(self.input_monto.text() or "0")
            if monto <= 0:
                raise ValueError()
        except:
            QMessageBox.warning(self, "Validación", "Monto inválido.")
            return False

        # Fecha límite
        sy = self.spin_year.value()
        sm = int(self.combo_month.currentText())
        ahora = datetime.now()
        if sy < ahora.year or (sy == ahora.year and sm < ahora.month):
            QMessageBox.warning(self, "Validación", "Fecha límite debe ser futura o actual.")
            return False

        return True

    # ------------------------------
    # Guardar meta
    # ------------------------------
    def guardar_meta(self):
        if not self.validar_form():
            return

        nombre = self.input_nombre.text().strip()
        monto = float(self.input_monto.text())
        subcat = self.combo_subcat.currentText()
        estado = self.combo_estado.currentText()
        mes = int(self.combo_month.currentText())
        año = self.spin_year.value()

        global metas_ahorro

        if self.editing_id is None:
            nueva = {
                "id": str(int(datetime.now().timestamp()*1000)),
                "nombre": nombre,
                "monto": monto,
                "subcategoria": subcat,
                "estado": estado,
                "mes": mes,
                "año": año
            }
            metas_ahorro.append(nueva)
            QMessageBox.information(self, "Meta de Ahorro", "Meta creada correctamente.")
        else:
            for m in metas_ahorro:
                if m["id"] == self.editing_id:
                    m.update({
                        "nombre": nombre,
                        "monto": monto,
                        "subcategoria": subcat,
                        "estado": estado,
                        "mes": mes,
                        "año": año
                    })
            QMessageBox.information(self, "Meta de Ahorro", "Meta actualizada.")
            self.editing_id = None

        self.limpiar_form()
        self.actualizar_tabla()

    # ------------------------------
    # Limpiar formulario
    # ------------------------------
    def limpiar_form(self):
        self.input_nombre.clear()
        self.input_monto.clear()
        self.spin_year.setValue(datetime.now().year)
        self.combo_month.setCurrentIndex(datetime.now().month-1)
        self.combo_subcat.setCurrentIndex(0)
        self.combo_estado.setCurrentIndex(0)
        self.editing_id = None

    # ------------------------------
    # Tabla
    # ------------------------------
    def actualizar_tabla(self):
        self.table.setRowCount(0)
        for m in metas_ahorro:
            row = self.table.rowCount()
            self.table.insertRow(row)

            self.table.setItem(row, 0, QTableWidgetItem(m["id"]))
            self.table.setItem(row, 1, QTableWidgetItem(m["nombre"]))
            self.table.setItem(row, 2, QTableWidgetItem(f"{m['monto']:.2f}"))
            self.table.setItem(row, 3, QTableWidgetItem(f"{m['mes']:02d}/{m['año']}"))
            self.table.setItem(row, 4, QTableWidgetItem(m["subcategoria"]))
            self.table.setItem(row, 5, QTableWidgetItem(m["estado"]))

            # Acciones
            btn_edit = QPushButton("Editar"); btn_edit.setStyleSheet(BTN_GRAY)
            btn_del = QPushButton("Eliminar"); btn_del.setStyleSheet(BTN_DANGER)

            btn_edit.clicked.connect(lambda checked, mid=m["id"]: self.cargar_edicion(mid))
            btn_del.clicked.connect(lambda checked, mid=m["id"]: self.eliminar(mid))

            cont = QWidget()
            hl = QHBoxLayout()
            hl.setContentsMargins(0,0,0,0)
            hl.addWidget(btn_edit)
            hl.addWidget(btn_del)
            cont.setLayout(hl)
            self.table.setCellWidget(row, 6, cont)

    # ------------------------------
    # Editar
    # ------------------------------
    def cargar_edicion(self, mid):
        for m in metas_ahorro:
            if m["id"] == mid:
                self.editing_id = mid
                self.input_nombre.setText(m["nombre"])
                self.input_monto.setText(str(m["monto"]))
                self.spin_year.setValue(m["año"])
                self.combo_month.setCurrentIndex(m["mes"]-1)
                self.combo_subcat.setCurrentText(m["subcategoria"])
                self.combo_estado.setCurrentText(m["estado"])
                break

    # ------------------------------
    # Eliminar
    # ------------------------------
    def eliminar(self, mid):
        global metas_ahorro
        r = QMessageBox.question(self, "Eliminar", "¿Eliminar esta meta?",
                                 QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if r == QMessageBox.StandardButton.Yes:
            metas_ahorro = [m for m in metas_ahorro if m["id"] != mid]
            self.actualizar_tabla()
