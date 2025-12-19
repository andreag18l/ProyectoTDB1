from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QFormLayout, QMessageBox,
    QStackedWidget
)
from PyQt6.QtCore import Qt
import sys

# ------------------------------
# SERVICIOS
# ------------------------------
from usuarios_service import crear_usuario, listar_usuarios

# ------------------------------
# PÁGINAS
# ------------------------------
from presupuesto_page import PresupuestoPage
from categorias_page import CategoriasPage
from transacciones_page import TransaccionesPage
from metas_ahorro_page import MetasAhorroPage
from reportes_page import ReportesPage
from dashboard_page import DashboardPage


# ------------------------------
# ESTILOS
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

TITLE_STYLE = "font-size: 20px; font-weight: bold;"


# ======================================================
# PÁGINAS DE AUTENTICACIÓN
# ======================================================

class InicioPage(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.usuario_activo = None

        title = QLabel("Finanzas Personales")
        title.setStyleSheet(TITLE_STYLE)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn_registro = QPushButton("Crear Cuenta")
        btn_registro.setStyleSheet(BTN_GRAY)
        btn_registro.clicked.connect(lambda: app.show_page("registro"))

        btn_login = QPushButton("Iniciar Sesión")
        btn_login.setStyleSheet(BTN_GRAY)
        btn_login.clicked.connect(lambda: app.show_page("login"))

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(btn_registro)
        layout.addWidget(btn_login)
        self.setLayout(layout)


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

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(btn)
        self.setLayout(layout)

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
            QMessageBox.information(self, "OK", "Usuario registrado correctamente")
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

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Correo"))
        layout.addWidget(self.correo)
        layout.addWidget(QLabel("Contraseña"))
        layout.addWidget(self.password)
        layout.addWidget(btn)
        self.setLayout(layout)

    def login(self):
     usuarios = listar_usuarios()
     for u in usuarios:
        if u[3] == self.correo.text():  # columna 3 = correo
            self.app.usuario_activo = u    
            self.app.show_page("dashboard")
            return
     QMessageBox.critical(self, "Error", "Usuario no encontrado")



# ======================================================
# APP PRINCIPAL
# ======================================================

class AppWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Presupuesto")
        self.stack = QStackedWidget() 
        self.pages = {
            "inicio": InicioPage(self),
            "registro": RegistroPage(self),
            "login": LoginPage(self),
            "dashboard": DashboardPage(self),
            "presupuesto": PresupuestoPage(self),
            "transacciones": TransaccionesPage(self),
            "categorías": CategoriasPage(self),
            "metas": MetasAhorroPage(self),
            "reportes": ReportesPage(self),
        }

        for page in self.pages.values():
            self.stack.addWidget(page)

        layout = QVBoxLayout()
        layout.addWidget(self.stack)
        self.setLayout(layout)

        self.show_page("inicio")

    def show_page(self, key):
        self.stack.setCurrentWidget(self.pages[key])


# ======================================================
# MAIN
# ======================================================

def main():
    app = QApplication(sys.argv)
    win = AppWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
