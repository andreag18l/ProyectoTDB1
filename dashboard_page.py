from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QFrame
)
from PyQt6.QtCore import Qt


class DashboardPage(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app

        # ---------- LAYOUT PRINCIPAL ----------
        main_layout = QHBoxLayout(self)

        # ---------- MENÚ LATERAL ----------
        menu = QVBoxLayout()
        menu.setSpacing(15)

        titulo = QLabel("Sistema de Gestión Financiera")
        titulo.setStyleSheet("font-size:16px; font-weight:bold;")
        menu.addWidget(titulo)

        botones = {
            "Dashboard": "dashboard",
            "Categorías": "categorías",
            "Presupuestos": "presupuesto",
            "Transacciones": "transacciones",
            "Metas de Ahorro": "metas",
            "Reportes": "reportes"
        }

        for texto, page in botones.items():
            b = QPushButton(texto)
            b.setStyleSheet("padding:10px; text-align:left;")
            b.clicked.connect(lambda _, p=page: app.show_page(p))
            menu.addWidget(b)

        btn_logout = QPushButton("Cerrar Sesión")
        btn_logout.setStyleSheet("background:#b91c1c; color:white; padding:10px;")
        btn_logout.clicked.connect(lambda: app.show_page("inicio"))
        menu.addStretch()
        menu.addWidget(btn_logout)

        menu_frame = QFrame()
        menu_frame.setLayout(menu)
        menu_frame.setFixedWidth(220)
        menu_frame.setStyleSheet("background:#f8f9fa;")

        # ---------- CONTENIDO CENTRAL ----------
        contenido = QVBoxLayout()

        titulo_central = QLabel("Metas de Ahorro")
        titulo_central.setStyleSheet("font-size:22px; font-weight:bold;")

        subtitulo = QLabel("Define y alcanza tus objetivos financieros")
        subtitulo.setStyleSheet("color:gray;")

        # Tarjetas
        cards = QHBoxLayout()

        cards.addWidget(self.card("Progreso Total", "0%", "$0 de $0"))
        cards.addWidget(self.card("Metas Activas", "0", "En progreso"))
        cards.addWidget(self.card("Metas Completadas", "0", "Logradas"))

        contenido.addWidget(titulo_central)
        contenido.addWidget(subtitulo)
        contenido.addSpacing(20)
        contenido.addLayout(cards)
        contenido.addStretch()

        main_layout.addWidget(menu_frame)
        main_layout.addLayout(contenido)

    def card(self, titulo, valor, detalle):
        box = QFrame()
        box.setStyleSheet("""
            QFrame {
                border:1px solid #ddd;
                border-radius:10px;
                padding:15px;
            }
        """)

        v = QVBoxLayout(box)

        t = QLabel(titulo)
        t.setStyleSheet("font-weight:bold;")

        v1 = QLabel(valor)
        v1.setStyleSheet("font-size:20px; color:#2563eb;")

        d = QLabel(detalle)
        d.setStyleSheet("color:gray;")

        v.addWidget(t)
        v.addWidget(v1)
        v.addWidget(d)

        return box
