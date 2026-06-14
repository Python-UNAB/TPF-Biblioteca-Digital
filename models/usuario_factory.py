from abc import ABC, abstractmethod
from models.usuario import Alumno, Profesor


class UsuarioFactory(ABC):
    """
    Creador Abstracto para la jerarquia de Usuarios.
    """

    @abstractmethod
    def crear_usuario(self, nombre: str, apellido: str, dni: int, correo: str):
        """
        Factory Method abstracto
        """
        pass


class AlumnoFactory(UsuarioFactory):
    """
    Fabrica concreta para Alumnos.
    """

    def crear_usuario(self, nombre: str, apellido: str, dni: int, correo: str):
        return Alumno(nombre, apellido, dni, correo)


class ProfesorFactory(UsuarioFactory):
    """
    Fabrica concreta para Profesores
    """

    def crear_usuario(self, nombre: str, apellido: str, dni: int, correo: str):
        return Profesor(nombre, apellido, dni, correo)
