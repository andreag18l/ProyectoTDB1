# categorias_page.py
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QFormLayout, QMessageBox, QTableWidget, QTableWidgetItem, QComboBox,
    QHeaderView, QGroupBox, QInputDialog
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from datetime import datetime

# ----------------------
# Estilos
# ----------------------
BTN_GRAY = """
    QPushButton {
        background-color: #f0f0f0;
        border: 1px solid #d0d0d0;
        border-radius: 8px;
        padding: 6px 10px;
        font-size: 14px;
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
        padding: 6px 10px;
        font-size: 14px;
    }
    QPushButton:hover {
        background-color: #991616;
    }
"""

INPUT_STYLE = """
    QLineEdit, QComboBox {
        padding: 6px;
        border-radius: 6px;
        border: 1px solid #cfcfcf;
        font-size: 14px;
    }
"""

WINDOW_BG = "background-color: #ffffff; color: #222222; font-family: Arial;"
TITLE_STYLE = "font-size: 20px; font-weight: bold; color: #2b2b2b;"

# ----------------------
# Lista de categorías en memoria
# ----------------------
categorias = []  # cada categoría: {id, nombre, tipo, subcategorias: [{"nombre": "General"}]}

class CategoriasPage(QWidget):
    def __init__(self, app_window):
        super().__init__()
        self.app_window = app_window
        self.setStyleSheet(WINDOW_BG)
        self.editing_id = None

        # ------------------------------
        # Título
        # ------------------------------
        title = QLabel("Gestión de Categorías")
        title.setFont(QFont("Arial", 18))
        title.setStyleSheet(TITLE_STYLE)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ------------------------------
        # Formulario
        # ------------------------------
        form_group = QGroupBox("Crear / Editar Categoría")
        form_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        form_layout = QFormLayout()

        self.input_nombre = QLineEdit(); self.input_nombre.setFixedWidth(300); self.input_nombre.setStyleSheet(INPUT_STYLE)
        self.combo_tipo = QComboBox(); self.combo_tipo.addItems(["Ingreso", "Gasto", "Ahorro"]); self.combo_tipo.setFixedWidth(150)

        form_layout.addRow("Nombre:", self.input_nombre)
        form_layout.addRow("Tipo:", self.combo_tipo)

        # Botones
        btn_guardar = QPushButton("Guardar"); btn_guardar.setStyleSheet(BTN_GRAY); btn_guardar.clicked.connect(self.guardar_categoria)
        btn_limpiar = QPushButton("Limpiar"); btn_limpiar.setStyleSheet(BTN_GRAY); btn_limpiar.clicked.connect(self.limpiar_form)
        btn_atras = QPushButton("Atrás"); btn_atras.setStyleSheet(BTN_GRAY); btn_atras.clicked.connect(lambda: self.app_window.show_page("dashboard"))

        h_buttons = QHBoxLayout()
        h_buttons.addWidget(btn_atras)
        h_buttons.addWidget(btn_limpiar)
        h_buttons.addWidget(btn_guardar)
        form_layout.addRow(h_buttons)

        form_group.setLayout(form_layout)

        # ------------------------------
        # Tabla
        # ------------------------------
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Tipo", "Subcategorías"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setColumnHidden(0, True)  # ocultar id
        self.table.setEditTriggers(self.table.EditTrigger.NoEditTriggers)

        # ------------------------------
        # Layout global
        # ------------------------------
        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(form_group)
        layout.addWidget(QLabel("Lista de Categorías:"))
        layout.addWidget(self.table)
        self.setLayout(layout)

        self.actualizar_tabla()

    # =====================================================
    # Validación
    # =====================================================
    def validar_form(self):
        nombre = self.input_nombre.text().strip()
        if not nombre:
            QMessageBox.warning(self, "Validación", "Debes ingresar un nombre de categoría.")
            return False
        return True

    # =====================================================
    # Guardar categoría
    # =====================================================
    def guardar_categoria(self):
        if not self.validar_form():
            return

        nombre = self.input_nombre.text().strip()
        tipo = self.combo_tipo.currentText()
        global categorias

        if self.editing_id is None:
            # Crear nueva categoría con subcategoría por defecto
            nueva = {
                "id": str(int(datetime.now().timestamp()*1000)),
                "nombre": nombre,
                "tipo": tipo,
                "subcategorias": [{"nombre": "General"}]  # trigger implícito
            }
            categorias.append(nueva)
            QMessageBox.information(self, "Categoría", f"Categoría '{nombre}' creada con subcategoría 'General'.")
        else:
            # Editar
            for c in categorias:
                if c["id"] == self.editing_id:
                    c["nombre"] = nombre
                    c["tipo"] = tipo
            QMessageBox.information(self, "Categoría", "Categoría actualizada.")
            self.editing_id = None

        self.limpiar_form()
        self.actualizar_tabla()

    # =====================================================
    # Limpiar formulario
    # =====================================================
    def limpiar_form(self):
        self.input_nombre.clear()
        self.combo_tipo.setCurrentIndex(0)
        self.editing_id = None

    # =====================================================
    # Tabla
    # =====================================================
    def actualizar_tabla(self):
        self.table.setRowCount(0)
        for c in categorias:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(c["id"]))
            self.table.setItem(row, 1, QTableWidgetItem(c["nombre"]))
            self.table.setItem(row, 2, QTableWidgetItem(c["tipo"]))

            # Subcategorías con botones
            cont = QWidget()
            hl = QHBoxLayout()
            hl.setContentsMargins(0,0,0,0)
            for s in c["subcategorias"]:
                btn_sub = QPushButton(s["nombre"])
                btn_sub.setStyleSheet(BTN_GRAY)
                btn_sub.clicked.connect(lambda checked, cid=c["id"], sname=s["nombre"]: self.eliminar_subcategoria(cid, sname))
                hl.addWidget(btn_sub)
            # Botón agregar
            btn_add = QPushButton("+")
            btn_add.setStyleSheet(BTN_GRAY)
            btn_add.clicked.connect(lambda checked, cid=c["id"]: self.agregar_subcategoria(cid))
            hl.addWidget(btn_add)

            cont.setLayout(hl)
            self.table.setCellWidget(row, 3, cont)

    # =====================================================
    # Agregar subcategoría
    # =====================================================
    def agregar_subcategoria(self, categoria_id):
        for c in categorias:
            if c["id"] == categoria_id:
                nombre, ok = QInputDialog.getText(self, "Nueva Subcategoría", "Nombre de la subcategoría:")
                if ok and nombre.strip():
                    c["subcategorias"].append({"nombre": nombre.strip()})
                    QMessageBox.information(self, "Subcategoría", f"Subcategoría '{nombre}' agregada.")
                    self.actualizar_tabla()
                break

    # =====================================================
    # Eliminar subcategoría
    # =====================================================
    def eliminar_subcategoria(self, categoria_id, subcat_nombre):
        for c in categorias:
            if c["id"] == categoria_id:
                if len(c["subcategorias"]) == 1:
                    QMessageBox.warning(self, "Regla de negocio", "No se puede eliminar la última subcategoría.")
                    return
                c["subcategorias"] = [s for s in c["subcategorias"] if s["nombre"] != subcat_nombre]
                QMessageBox.information(self, "Subcategoría", f"Subcategoría '{subcat_nombre}' eliminada.")
                self.actualizar_tabla()
                break
