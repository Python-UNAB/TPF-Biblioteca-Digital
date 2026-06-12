from datetime import datetime
from models.entidad_base import EntidadBase
from models.usuario import Usuario
from models.recurso import Recurso


class Prestamo(EntidadBase):

    def __init__(self, usuario: Usuario, recurso: Recurso):
        super().__init__()
        self.usuario = usuario
        self.recurso = recurso
        self.fecha_prestamo = datetime.now()
        self.fecha_devolucion = None

    def finalizar_prestamo(self):
        self.fecha_devolucion = datetime.now( )

    def __repr__(self) -> str:
        return f"Prestamo(id={self.id}, Usuario={self.usuario.nombre} {self.usuario.apellido}, Recurso={self.recurso.titulo})"