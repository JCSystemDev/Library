import qdarkstyle
from PySide6.QtGui import QIcon, QPixmap, Qt
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

import mainwindow


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Biblioteca - Login")
        self.setGeometry(100, 100, 320, 450)
        self.username = "biblioteca"
        self.user_clave = "admin"

        # Aplicar estilo oscuro
        self.setStyleSheet(qdarkstyle.load_stylesheet())

        # Establecer el icono de la ventana
        self.setWindowIcon(QIcon("img/icon.ico"))

        # Crear widget de inicio de sesión
        widget = QWidget()
        layout = QVBoxLayout()

        # Agregar imagen superior
        image_label = QLabel()
        pixmap = QPixmap("img/login.png")
        pixmap = pixmap.scaled(256, 256, Qt.AspectRatioMode.KeepAspectRatio)
        image_label.setPixmap(pixmap)
        layout.addWidget(image_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Agregar espaciado vertical
        layout.addSpacing(0)

        label_username = QLabel("Usuario:")
        self.lineedit_username = QLineEdit()
        layout.addWidget(label_username, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lineedit_username, alignment=Qt.AlignmentFlag.AlignCenter)

        label_password = QLabel("Contraseña:")
        self.lineedit_password = QLineEdit()
        self.lineedit_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(label_password, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lineedit_password, alignment=Qt.AlignmentFlag.AlignCenter)

        button_login = QPushButton("Iniciar sesión")
        button_login.clicked.connect(self.login)
        layout.addWidget(button_login, alignment=Qt.AlignmentFlag.AlignCenter)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Referencia a la ventana principal
        self.main_window = None

    def login(self):
        username = self.lineedit_username.text()
        password = self.lineedit_password.text()

        # Lógica para verificar el usuario y contraseña
        if self.username == username and self.user_clave == password:
            # Si el inicio de sesión es exitoso, mostrar la ventana principal
            self.main_window = mainwindow.MainWindow()
            self.main_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Inicio de sesión fallido", "Usuario o contraseña incorrectos")
