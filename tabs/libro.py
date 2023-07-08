from formwindow import Buscar, Actualizar, Eliminar, Crear


class AgregarLibro(Crear):
    def __init__(self):
        self.collection_name = "libro"
        fields = ["_id", "titulo", "autores", "anio_publicacion", "descripcion", "editorial", "copias_disponibles"]
        headers = ["Código de Libro", "Título", "Autores", "Año de publicación", "Descripción", "Editorial",
                   "Copias disponibles"]
        super().__init__(self.collection_name, fields, headers)
        self.setWindowTitle("Biblioteca - Agregar Libro")
        self.title_label.setText("Agregar Libro")

    def create_and_exec(self):
        form = AgregarLibro()
        form.exec_()


class ActualizarLibro(Actualizar):
    def __init__(self):
        collection_name = "libro"
        fields = ["_id", "titulo", "autores", "anio_publicacion", "descripcion", "editorial", "copias_disponibles"]
        headers = ["Código de Libro", "Título", "Autores", "Año de publicación", "Descripción", "Editorial",
                   "Copias disponibles"]
        super().__init__(collection_name, fields, headers)
        self.setWindowTitle("Biblioteca - Actualizar Libro")
        self.title_label.setText("Actualizar Libro")

    def create_and_exec(self):
        form = ActualizarLibro()
        form.exec_()


class EliminarLibro(Eliminar):
    def __init__(self):
        collection_name = "libro"
        fields = ["_id", "titulo", "autores", "anio_publicacion", "descripcion", "editorial", "copias_disponibles"]
        headers = ["Código de Libro", "Título", "Autores", "Año de publicación", "Descripción", "Editorial",
                   "Copias disponibles"]
        super().__init__(collection_name, fields, headers)
        self.setWindowTitle("Biblioteca - Eliminar Libro")
        self.title_label.setText("Eliminar Libro")

    def create_and_exec(self):
        form = EliminarLibro()
        form.exec_()


class BuscarLibro(Buscar):
    def __init__(self):
        fields = ["_id", "titulo", "autores", "anio_publicacion", "descripcion", "editorial", "copias_disponibles"]
        headers = ["Código de Libro", "Título", "Autores", "Año de publicación", "Descripción", "Editorial",
                   "Copias disponibles"]
        super().__init__("libro", fields, headers)
        self.setWindowTitle("Biblioteca - Buscar Libro")
        self.title_label.setText("Buscar Libro")

    def create_and_exec(self):
        form = BuscarLibro()
        form.exec_()

