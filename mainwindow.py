from datetime import datetime

import qdarkstyle
from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon, QPixmap, Qt, QFont
from PySide6.QtWidgets import QMainWindow, QTabWidget, QHBoxLayout, QWidget, QPushButton, QVBoxLayout, QLabel, \
    QMessageBox
from pymongo import MongoClient

import dao
from tabs import libro, prestamo, lector


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Biblioteca - Main")
        self.setFixedSize(1024, 640)
        self.closed = Signal()

        # Aplicar estilo oscuro
        self.setStyleSheet(qdarkstyle.load_stylesheet())

        # Establecer el icono de la ventana
        self.setWindowIcon(QIcon("img/icon.ico"))

        self.tab_widget = QTabWidget()

        widget_container = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(self.tab_widget)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        widget_container.setLayout(layout)
        self.setCentralWidget(widget_container)

        self.create_tab(4, ["Agregar Libro", "Eliminar Libro",
                            "Actualizar Datos de Libro", "Buscar Libro"],
                        "Libro", "img/catalogo.png", "Catálogo de Libros",
                        [libro.AgregarLibro.create_and_exec, libro.EliminarLibro.create_and_exec,
                         libro.ActualizarLibro.create_and_exec, libro.BuscarLibro.create_and_exec])

        self.create_tab(4, ["Agregar Lector", "Eliminar Lector", "Actualizar Lector", "Buscar Lector"],
                        "Lector", "img/lector.png", "Gestión de Lectores",
                        [lector.AgregarLector.create_and_exec, lector.EliminarLector.create_and_exec,
                         lector.ActualizarLector.create_and_exec, lector.BuscarLector.create_and_exec])

        self.create_tab(4, ["Agregar Préstamo", "Eliminar Préstamo", "Actualizar Préstamo", "Buscar Préstamo"],
                        "Prestamo", "img/prestamo.png", "Gestión de Préstamos",
                        [prestamo.CrearPrestamo.create_and_exec, prestamo.EliminarPrestamo.create_and_exec,
                         prestamo.ActualizarPrestamo.create_and_exec, prestamo.BuscarPrestamo.create_and_exec])

        self.asignar_multas()

    def create_widget(self, num_buttons, button_names, name, image_path, description_text, button_functions):

        button_names = button_names[:num_buttons]

        buttons = []

        for name, func in zip(button_names, button_functions):
            button = QPushButton(name)
            button.clicked.connect(func)  # Asignar la función al evento clicked del botón
            buttons.append(button)

        widget = QWidget()
        layout = QVBoxLayout()

        description_label = QLabel(description_text)
        description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description_label.setFont(QFont("Arial", 20))
        layout.addWidget(description_label)

        image_label = QLabel()
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(256, 256, Qt.AspectRatioMode.KeepAspectRatio)
        image_label.setPixmap(pixmap)
        layout.addWidget(image_label, alignment=Qt.AlignmentFlag.AlignCenter)

        description_label.setContentsMargins(0, 0, 0, 40)
        # Ajustar los márgenes del layout (arriba, izquierda, abajo, derecha)

        image_label.setContentsMargins(0, 0, 0, 180)
        # Ajustar los márgenes de la imagen (arriba, izquierda, derecha, abajo)

        crud_layout = QHBoxLayout()
        crud_layout.setContentsMargins(0, 0, 0, 0)
        # Ajustar los márgenes de la capa de botones (arriba, izquierda, abajo, derecha)

        for button in buttons:
            crud_layout.addWidget(button)

        layout.addLayout(crud_layout)
        widget.setLayout(layout)
        return widget

    def create_tab(self, num_buttons, button_names, name, path, title, button_functions):
        widget = self.create_widget(num_buttons, button_names, name, path, title, button_functions)
        self.tab_widget.addTab(widget, name)

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, "¿Salir?",
            "¿Estás seguro de que deseas salir?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def asignar_multas(self):
        # Conexión a la base de datos
        client = MongoClient('localhost', 27017)
        db = client['biblioteca']
        prestamo_collection = db['prestamo']
        lector_collection = db['lector']

        # Obtener todos los préstamos
        prestamos = prestamo_collection.find()

        # Calcular y asignar la multa para cada préstamo
        for prestamo in prestamos:
            id_lector = prestamo["id_lector"]
            lector = lector_collection.find_one({"_id": id_lector})

            if lector and lector["prestamo"]:
                fecha_devolucion = datetime.strptime(prestamo["fecha_devolucion"], "%Y-%m-%d").date()
                diferencia_dias = (datetime.now().date() - fecha_devolucion).days
                if diferencia_dias > 0:
                    multa = diferencia_dias * 250
                    prestamo_collection.update_one({"_id": prestamo["_id"]}, {"$set": {"multa": multa}})

        # Cerrar conexión a la base de datos
        client.close()
