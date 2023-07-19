from datetime import datetime

import qdarkstyle
from PySide6.QtGui import QFont, QIcon, QPixmap
from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout, QPushButton, QWidget, QFormLayout, QLineEdit, QMessageBox, \
    QHBoxLayout, QGroupBox
from PySide6.QtCore import Qt

from dao import DAO


class FormWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(qdarkstyle.load_stylesheet())
        self.setWindowIcon(QIcon("img/icon.ico"))
        self.collection_name = ""
        self.fields = []
        self.headers = []
        self.widget = QWidget()
        self.layout = QVBoxLayout(self.widget)
        self.title_label = QLabel()
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setContentsMargins(0, -80, 0, -40)
        self.title_label.setFont(QFont("Arial", 20))
        self.layout.addWidget(self.title_label)
        self.image_label = QLabel()
        self.image_path = ""
        self.pixmap = QPixmap(self.image_path)
        self.pixmap = self.pixmap.scaled(128, 128)
        self.image_label.setPixmap(self.pixmap)
        self.layout.addWidget(self.image_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.image_label.setContentsMargins(0, -50, 0, 50)
        self.setLayout(self.layout)

    def set_title_text(self, text):
        self.title_label.setText(text)

    def update_image(self):
        self.pixmap = QPixmap(self.image_path)
        self.pixmap = self.pixmap.scaled(128, 128, Qt.AspectRatioMode.KeepAspectRatio)
        self.image_label.setPixmap(self.pixmap)

    def clear_line_edits(self):
        for line_edit in self.line_edits.values():
            line_edit.clear()

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def format_value(self, value):
        if isinstance(value, list):
            return ", ".join(str(item) for item in value)
        return str(value)

    def show_document_info(self, document):
        self.clear_layout(self.info_layout)

        for field, header in zip(self.fields, self.headers):
            label_text = header.capitalize()
            value_text = self.format_value(document.get(field, ""))
            label = QLabel(label_text)
            value_label = QLabel(value_text)
            value_label.setStyleSheet("font-weight: bold")

            self.info_layout.addRow(label, value_label)


class Crear(FormWindow):
    def __init__(self, collection_name, fields, headers):
        super().__init__()
        self.setFixedSize(480, 600)
        self.image_path = "img/crear.png"
        self.update_image()
        self.collection_name = collection_name
        self.title_label.setContentsMargins(0, -50, 0, 0)
        self.fields = fields
        self.form_layout = QFormLayout()
        self.layout.addLayout(self.form_layout)

        self.line_edits = {}
        for field, header in zip(self.fields, headers):
            label_text = header.replace("_", " ").capitalize()
            label = QLabel(label_text)
            line_edit = QLineEdit()
            self.form_layout.addRow(label, line_edit)
            self.line_edits[field] = line_edit

        self.agregar_button = QPushButton("Agregar")
        self.agregar_button.clicked.connect(self.insert_row)
        self.layout.addWidget(self.agregar_button)

    def insert_row(self):
        document = {}
        for field, line_edit in self.line_edits.items():
            value = line_edit.text()
            if field == "libros_prestados":
                value = [book.strip() for book in value.split(",")]
            if field == "autores":
                value = [autor.strip() for autor in value.split(",")]
            if field == "multa":
                value = 0
            if field == "prestamo":
                value = False
            document[field] = value

        dao = DAO()
        try:
            if self.collection_name == "prestamo":
                # Verificar si el lector ya tiene un préstamo realizado
                id_lector = document["id_lector"]
                lector = dao.buscar("lector", {"_id": id_lector})
                if lector and lector.get("prestamo", False):
                    QMessageBox.warning(self, "Error", "El lector ya tiene un préstamo realizado.")
                    return

                # Verificar disponibilidad de copias en la colección "libro"
                libros_prestados = document["libros_prestados"]
                libros = dao.mostrar("libro", {"_id": {"$in": libros_prestados}})
                for libro in libros:
                    if libro.get("copias_disponibles", 0) <= 0:
                        QMessageBox.warning(self, "Error", f"No hay copias disponibles del libro '{libro['_id']}'.")
                        return

                # Agregar el préstamo en la colección "prestamo"
                prestamo_id = dao.crear(self.collection_name, document)

                # Actualizar el campo "prestamo" en la colección "lector"
                dao.modificar("lector", {"_id": id_lector}, {"prestamo": True})

            else:
                # Insertar el documento en la colección respectiva
                dao.crear(self.collection_name, document)

            QMessageBox.information(self, "Éxito", f"{self.collection_name.capitalize()} agregado correctamente.")
            self.clear_line_edits()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo agregar el {self.collection_name}. Error: {str(e)}")

        dao.cerrar_conexion()


class Actualizar(FormWindow):
    def __init__(self, collection_name, fields, headers):
        super().__init__()
        self.setFixedSize(550, 600)
        self.image_path = "img/actualizar.png"
        self.update_image()
        self.title_label.setText("Actualizar")

        self.search_layout = QHBoxLayout()
        self.layout.addLayout(self.search_layout)

        self.search_label = QLabel("ID del documento:")
        self.search_layout.addWidget(self.search_label)

        self.search_line_edit = QLineEdit()
        self.search_layout.addWidget(self.search_line_edit)

        self.search_button = QPushButton("Buscar")
        self.search_button.clicked.connect(self.search_document)
        self.search_layout.addWidget(self.search_button)

        self.form_layout = QFormLayout()
        self.layout.addLayout(self.form_layout)

        self.line_edits = {}
        for field, header in zip(fields, headers):
            label_text = header.replace("_", " ").capitalize()
            label = QLabel(label_text)
            line_edit = QLineEdit()
            self.form_layout.addRow(label, line_edit)
            self.line_edits[field] = line_edit

        self.update_button = QPushButton("Actualizar")
        self.update_button.clicked.connect(self.update_document)
        self.layout.addWidget(self.update_button)

        self.collection_name = collection_name

    def search_document(self):
        document_id = self.search_line_edit.text()
        dao = DAO()
        result = dao.buscar(self.collection_name, {"_id": document_id})
        dao.cerrar_conexion()

        if result:
            for field, line_edit in self.line_edits.items():
                if field in ["autores", "libros_prestados"]:
                    line_edit.setText(", ".join(result[field]))
                else:
                    line_edit.setText(str(result[field]))
        else:
            QMessageBox.warning(self, "Error", "No se encontró el documento.")

    def update_document(self):
        document_id = self.search_line_edit.text()
        new_values = {}
        for field, line_edit in self.line_edits.items():
            if field in ["autores", "libros_prestados"]:
                new_values[field] = [item.strip() for item in line_edit.text().split(",")]
            else:
                new_values[field] = line_edit.text()

        dao = DAO()
        try:
            # Verificar si el campo "prestamo" pasó de True a False
            if self.collection_name == "lector":
                old_values = dao.buscar(self.collection_name, {"_id": document_id})
                if old_values and old_values.get("prestamo", False) and not new_values.get("prestamo", False):
                    # Obtener los libros prestados asociados al id_lector
                    prestamo_collection = dao.db["prestamo"]
                    prestamos = prestamo_collection.find({"id_lector": document_id})
                    libros_prestados = []
                    for prestamo in prestamos:
                        libros_prestados.extend(prestamo.get("libros_prestados", []))

                    # Actualizar las copias disponibles de los libros prestados
                    libro_collection = dao.db["libro"]
                    libro_collection.update_many({"_id": {"$in": libros_prestados}},
                                                 {"$inc": {"copias_disponibles": 1}})

            modified_count = dao.modificar(self.collection_name, {"_id": document_id}, new_values)
            if modified_count > 0:
                QMessageBox.information(self, "Éxito", "Documento actualizado correctamente.")
                self.clear_line_edits()
            else:
                QMessageBox.warning(self, "Error", "No se pudo actualizar el documento.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo actualizar el documento. Error: {str(e)}")

        dao.cerrar_conexion()


class Eliminar(FormWindow):
    def __init__(self, collection_name, fields, headers):
        super().__init__()
        self.setFixedSize(550, 600)
        self.image_path = "img/eliminar.png"
        self.update_image()
        self.collection_name = collection_name
        self.fields = fields
        self.headers = headers

        self.search_layout = QHBoxLayout()
        self.layout.addLayout(self.search_layout)

        self.search_label = QLabel(f"Código del {collection_name.capitalize()}:")
        self.search_layout.addWidget(self.search_label)

        self.search_line_edit = QLineEdit()
        self.search_layout.addWidget(self.search_line_edit)

        self.search_button = QPushButton("Buscar")
        self.search_button.clicked.connect(self.search_document)
        self.search_layout.addWidget(self.search_button)

        self.info_groupbox = QGroupBox(f"Información del {collection_name.capitalize()}")
        self.info_layout = QFormLayout(self.info_groupbox)
        self.layout.addWidget(self.info_groupbox)

        self.delete_button = QPushButton("Eliminar")
        self.delete_button.clicked.connect(self.delete_document)
        self.delete_button.setEnabled(False)
        self.layout.addWidget(self.delete_button)

    def search_document(self):
        document_id = self.search_line_edit.text()
        dao = DAO()
        result = dao.buscar(self.collection_name, {"_id": document_id})
        dao.cerrar_conexion()

        if result:
            self.show_document_info(result)
            self.delete_button.setEnabled(True)
        else:
            QMessageBox.warning(self, "Error", f"No se encontró el {self.collection_name.capitalize()}.")

    def show_document_info(self, document):
        self.clear_layout(self.info_layout)

        for field, header in zip(self.fields, self.headers):
            label_text = header.capitalize()
            value_text = self.format_value(document.get(field, ""))
            label = QLabel(label_text)
            value_label = QLabel(value_text)
            value_label.setStyleSheet("font-weight: bold")

            self.info_layout.addRow(label, value_label)

    def add_info_label(self, label_text, value_text):
        label = QLabel(label_text)
        value_label = QLabel(value_text)
        value_label.setStyleSheet("font-weight: bold")

        self.info_layout.addRow(label, value_label)

    def delete_document(self):
        document_id = self.search_line_edit.text()
        dao = DAO()
        result = dao.eliminar(self.collection_name, {"_id": document_id})
        dao.cerrar_conexion()

        if result > 0:
            QMessageBox.information(self, "Éxito", f"{self.collection_name.capitalize()} eliminado correctamente.")
        else:
            QMessageBox.warning(self, "Error", f"No se pudo eliminar el {self.collection_name.capitalize()}.")

        self.close()


class Buscar(FormWindow):
    def __init__(self, collection_name, fields, headers):
        super().__init__()
        self.setWindowTitle(f"Biblioteca - Buscar {collection_name.capitalize()}")
        self.image_path = "img/buscar.png"
        self.update_image()
        self.title_label.setText("Buscar")

        self.collection_name = collection_name
        self.fields = fields
        self.headers = headers

        self.search_layout = QHBoxLayout()
        self.layout.addLayout(self.search_layout)

        self.search_label = QLabel("Código del documento:")
        self.search_layout.addWidget(self.search_label)

        self.search_line_edit = QLineEdit()
        self.search_layout.addWidget(self.search_line_edit)

        self.search_button = QPushButton("Buscar")
        self.search_button.clicked.connect(self.search_document)
        self.search_layout.addWidget(self.search_button)

        self.info_groupbox = QGroupBox(f"Información del {collection_name.capitalize()}")
        self.info_layout = QFormLayout(self.info_groupbox)
        self.layout.addWidget(self.info_groupbox)

    def search_document(self):
        document_id = self.search_line_edit.text()
        dao = DAO()
        result = dao.buscar(self.collection_name, {"_id": document_id})
        dao.cerrar_conexion()

        if result:
            self.show_document_info(result)
        else:
            QMessageBox.warning(self, "Error", f"No se encontró el {self.collection_name}.")

