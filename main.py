from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QFormLayout, QMessageBox,
    QStackedWidget, QScrollArea
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
import sys

# IMPORTANTE: conexión real a BD
from usuarios_service import crear_usuario
from usuarios_service import listar_usuarios  # solo para login simple

from presupuesto_page import PresupuestoPage
from categorias_page import CategoriasPage
from transacciones_page import TransaccionesPage
from metas_ahorro_page import MetasAhorroPage


# ------------------------------
# Estilos
# ------------------------------
BTN_GRAY = """
QPushButton {
    background-color: #f0f0f0;
    border: 1px solid #d0d0d0;
    border-radius: 8px;
    padding: 10px;
}
QPushButton:hover { background-color: #e6e6e6; }
"""

BTN_DANGER = """
QPushButton {
    background-color: #b91c1c;
    color: white;
    border-radius: 8px;
    padding: 10px;
}
"""

INPUT_STYLE = """
QLineEdit {
    padding: 8px;
    border-radius: 6px;
    border: 1px solid #cfcfcf;
}
"""

WINDOW_BG = "background-color: white;"
TITLE_STYLE = "font-size: 20px; font-weight: bold;"


# ------------------------------
# PÁGINAS
# ------------------------------
class InicioPage(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app

        title = QLabel("Finanzas Personales")
        title.setStyleSheet(TITLE_STYLE)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn_registro = QPushButton("Crear Cuenta")
        btn_registro.setStyleSheet(BTN_GRAY)
        btn_registro.clicked.connect(lambda: app.show_page("registro"))

        btn_login = QPushButton("Iniciar Sesión")
        btn_login.setStyleSheet(BTN_GRAY)
        btn_login.clicked.connect(lambda: app.show_page("login"))

        v = QVBoxLayout()
        v.addWidget(title)
        v.addWidget(btn_registro)
        v.addWidget(btn_login)
        self.setLayout(v)


class RegistroPage(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app

        self.nombre = QLineEdit()
        self.apellido = QLineEdit()
        self.correo = QLineEdit()
        self.salario = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        for w in (self.nombre, self.apellido, self.correo, self.salario, self.password):
            w.setStyleSheet(INPUT_STYLE)

        form = QFormLayout()
        form.addRow("Nombre", self.nombre)
        form.addRow("Apellido", self.apellido)
        form.addRow("Correo", self.correo)
        form.addRow("Salario", self.salario)
        form.addRow("Contraseña", self.password)

        btn = QPushButton("Registrar")
        btn.setStyleSheet(BTN_GRAY)
        btn.clicked.connect(self.registrar)

        v = QVBoxLayout()
        v.addLayout(form)
        v.addWidget(btn)
        self.setLayout(v)

    def registrar(self):
        try:
            crear_usuario(
                self.nombre.text(),
                self.apellido.text(),
                self.correo.text(),
                float(self.salario.text()),
                "ACTIVO",
                "frontend"
            )
            QMessageBox.information(self, "OK", "Usuario registrado en la BD")
            self.app.show_page("login")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


class LoginPage(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app

        self.correo = QLineEdit()
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        for w in (self.correo, self.password):
            w.setStyleSheet(INPUT_STYLE)

        btn = QPushButton("Entrar")
        btn.setStyleSheet(BTN_GRAY)
        btn.clicked.connect(self.login)

        v = QVBoxLayout()
        v.addWidget(QLabel("Correo"))
        v.addWidget(self.correo)
        v.addWidget(QLabel("Contraseña"))
        v.addWidget(self.password)
        v.addWidget(btn)
        self.setLayout(v)

    def login(self):
        usuarios = listar_usuarios()
        for u in usuarios:
            if u[3] == self.correo.text():
                self.app.show_page("menu")
                return
        QMessageBox.critical(self, "Error", "Usuario no encontrado")


class MenuPage(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app

        v = QVBoxLayout()
        for op in ["Presupuesto", "Transacciones", "Categorías", "Metas", "Reportes"]:
            b = QPushButton(op)
            b.setStyleSheet(BTN_GRAY)
            b.clicked.connect(lambda _, o=op: app.show_page(o.lower()))
            v.addWidget(b)

        btn_logout = QPushButton("Cerrar Sesión")
        btn_logout.setStyleSheet(BTN_DANGER)
        btn_logout.clicked.connect(lambda: app.show_page("inicio"))
        v.addWidget(btn_logout)

        self.setLayout(v)


# ------------------------------
# APP
# ------------------------------
class AppWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Presupuesto")
        self.stack = QStackedWidget()

        self.pages = {
            "inicio": InicioPage(self),
            "registro": RegistroPage(self),
            "login": LoginPage(self),
            "menu": MenuPage(self),
            "presupuesto": PresupuestoPage(self),
            "transacciones": TransaccionesPage(self),
            "categorías": CategoriasPage(self),
            "metas": MetasAhorroPage(self),
            "reportes": QWidget(),
        }

        for p in self.pages.values():
            self.stack.addWidget(p)

        layout = QVBoxLayout()
        layout.addWidget(self.stack)
        self.setLayout(layout)

        self.show_page("inicio")

    def show_page(self, key):
        self.stack.setCurrentWidget(self.pages[key])


def main():
    app = QApplication(sys.argv)
    win = AppWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
