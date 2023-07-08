from formwindow import Buscar, Actualizar, Eliminar, Crear


class AgregarLector(Crear):
    def __init__(self):
        collection_name = "lector"
        fields = ["_id", "nombre", "apellido", "rut", "email", "telefono", "prestamo"]
        headers = ["Código de Lector", "Nombre", "Apellido", "RUT", "Email", "Teléfono", "Prestamo"]
        super().__init__(collection_name, fields, headers)
        self.setWindowTitle("Biblioteca - Agregar Lector")
        self.title_label.setText("Agregar Lector")

    def create_and_exec(self):
        form = AgregarLector()
        form.exec_()


class ActualizarLector(Actualizar):
    def __init__(self):
        collection_name = "lector"
        fields = ["_id", "nombre", "apellido", "rut", "email", "telefono", "prestamo"]
        headers = ["Código de Lector", "Nombre", "Apellido", "RUT", "Email", "Teléfono", "Prestamo"]
        super().__init__(collection_name, fields, headers)
        self.setWindowTitle("Biblioteca - Actualizar Lector")
        self.title_label.setText("Actualizar Lector")

    def create_and_exec(self):
        form = ActualizarLector()
        form.exec_()


class EliminarLector(Eliminar):
    def __init__(self):
        collection_name = "lector"
        fields = ["_id", "nombre", "apellido", "rut", "email", "telefono", "prestamo"]
        headers = ["Código de Lector", "Nombre", "Apellido", "RUT", "Email", "Teléfono", "Préstamo"]
        super().__init__(collection_name, fields, headers)
        self.setWindowTitle("Biblioteca - Eliminar Lector")
        self.title_label.setText("Eliminar Lector")

    def create_and_exec(self):
        form = EliminarLector()
        form.exec_()


class BuscarLector(Buscar):
    def __init__(self):
        fields = ["_id", "nombre", "apellido", "rut", "email", "telefono", "prestamo"]
        headers = ["Código de Lector", "Nombre", "Apellido", "RUT", "Email", "Teléfono", "Prestamo"]
        super().__init__("lector", fields, headers)
        self.setWindowTitle("Biblioteca - Buscar Lector")
        self.title_label.setText("Buscar Lector")

    def create_and_exec(self):
        form = BuscarLector()
        form.exec_()

