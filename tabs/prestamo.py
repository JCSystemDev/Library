from formwindow import Buscar, Actualizar, Eliminar, Crear


class CrearPrestamo(Crear):
    def __init__(self):
        collection_name = "prestamo"
        fields = ["_id", "libros_prestados", "id_lector", "fecha_prestamo", "fecha_devolucion", "multa"]
        headers = ["Código de Préstamo", "Libros Prestados", "Código de Lector", "Fecha de Préstamo",
                   "Fecha de Devolución", "Multa"]
        super().__init__(collection_name, fields, headers)
        self.setWindowTitle("Biblioteca - Agregar Préstamo")
        self.title_label.setText("Agregar Préstamo")

    def create_and_exec(self):
        form = CrearPrestamo()
        form.exec_()


class ActualizarPrestamo(Actualizar):
    def __init__(self):
        collection_name = "prestamo"
        fields = ["_id", "libros_prestados", "id_lector", "fecha_prestamo", "fecha_devolucion", "multa"]
        headers = ["Código de Préstamo", "Libros Prestados", "Código de Lector", "Fecha de Préstamo",
                   "Fecha de Devolución", "Multa"]
        super().__init__(collection_name, fields, headers)
        self.setWindowTitle("Biblioteca - Actualizar Préstamo")
        self.title_label.setText("Actualizar Préstamo")

    def create_and_exec(self):
        form = ActualizarPrestamo()
        form.exec_()


class EliminarPrestamo(Eliminar):
    def __init__(self):
        collection_name = "prestamo"
        fields = ["_id", "libros_prestados", "id_lector", "fecha_prestamo", "fecha_devolucion", "multa"]
        headers = ["Código de Préstamo", "Libros Prestados", "Código de Lector", "Fecha de Préstamo",
                   "Fecha de Devolución", "Multa"]
        super().__init__(collection_name, fields, headers)
        self.setWindowTitle("Biblioteca - Eliminar Préstamo")
        self.title_label.setText("Eliminar Préstamo")

    def create_and_exec(self):
        form = EliminarPrestamo()
        form.exec_()


class BuscarPrestamo(Buscar):
    def __init__(self):
        fields = ["_id", "libros_prestados", "id_lector", "fecha_prestamo", "fecha_devolucion", "multa"]
        headers = ["ID", "Libros Prestados", "ID Lector", "Fecha de Préstamo", "Fecha de Devolución", "Multa"]
        super().__init__("prestamo", fields, headers)
        self.setWindowTitle("Biblioteca - Buscar Préstamo")
        self.title_label.setText("Buscar Préstamo")

    def create_and_exec(self):
        form = BuscarPrestamo()
        form.exec_()
