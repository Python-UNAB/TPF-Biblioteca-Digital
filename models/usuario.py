from abc import abstractmethod
from models.entidad_base import EntidadBase


class Usuario(EntidadBase):
    """
    Clase base para usuarios. Actua como 'Observer'.
    """

    def __init__(self, nombre: str, apellido: str, dni: int, correo: str):
        super().__init__()
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.correo = correo

    def actualizar_notificacion(self, recurso):
        """
        Método del patrón Observer llamado por el Sujeto.
        """
        print(f"Notificacion enviada a: {self.correo}\nEl recurso '{recurso.titulo}' ya se encuentra disponible.")

    @abstractmethod
    def limite_prestamos(self) -> int:
        pass


class Alumno(Usuario):
    def limite_prestamos(self) -> int:
        return 3


class Profesor(Usuario):
    def limite_prestamos(self) -> int:
        return 5