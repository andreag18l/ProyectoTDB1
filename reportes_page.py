from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QMessageBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from reportes_service import reporte_resumen_mensual, reporte_gastos_por_descripcion

BTN_GRAY = """
QPushButton {
    background-color: #f0f0f0;
    border-radius: 8px;
    padding: 10px;
}
"""

class ReportesPage(QWidget):
    def __init__(self, app_window):
        super().__init__()
        self.app_window = app_window

        title = QLabel("Reportes Financieros")
        title.setFont(QFont("Arial", 18))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Botones para cada reporte
        btn_reporte1 = QPushButton("Reporte 1: Resumen Mensual")
        btn_reporte1.setStyleSheet(BTN_GRAY)
        btn_reporte1.clicked.connect(self.generar_reporte1)

        btn_reporte2 = QPushButton("Reporte 2: Distribución de Gastos")
        btn_reporte2.setStyleSheet(BTN_GRAY)
        btn_reporte2.clicked.connect(self.generar_reporte2)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(btn_reporte1)
        layout.addWidget(btn_reporte2)
        self.setLayout(layout)

    def generar_reporte1(self):
        try:
            if not hasattr(self.app_window, "usuario_activo") or not self.app_window.usuario_activo:
                QMessageBox.warning(self, "Atención", "No hay usuario activo.")
                return

            id_usuario = self.app_window.usuario_activo[0]
            reporte_resumen_mensual(id_usuario)
            QMessageBox.information(self, "Éxito", "Reporte 1 generado correctamente.\nArchivo PDF creado.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo generar el Reporte 1:\n{e}")

    def generar_reporte2(self):
        try:
            if not hasattr(self.app_window, "usuario_activo") or not self.app_window.usuario_activo:
                QMessageBox.warning(self, "Atención", "No hay usuario activo.")
                return

            id_usuario = self.app_window.usuario_activo[0]
            reporte_gastos_por_descripcion(id_usuario)
            QMessageBox.information(self, "Éxito", "Reporte 2 generado correctamente.\nArchivo PDF creado.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo generar el Reporte 2:\n{e}")
