from abc import ABC, abstractmethod
from models.recurso import Libro, AudioLibro


class RecursoFactory(ABC):
    """
    Creador abstracto para la jerarquía de Recursos.
    """

    @abstractmethod
    def crear_recurso(self, **kwargs):
        """
        Factory Method abstracto
        """
        pass


class LibroFactory(RecursoFactory):
    """
    Fabrica concreta para Libros
    """

    def crear_recurso(self, **kwargs):
        return Libro(
            titulo=kwargs['titulo'],
            autor=kwargs['autor'],
            anio=kwargs['anio'],
            isbn=kwargs['isbn'],
            paginas=kwargs['paginas']
        )


class AudioLibroFactory(RecursoFactory):
    """
    Fabrica concreta para AudioLibros
    """

    def crear_recurso(self, **kwargs):
        return AudioLibro(
            titulo=kwargs['titulo'],
            autor=kwargs['autor'],
            anio=kwargs['anio'],
            duracion_minutos=kwargs['duracion_minutos'],
            formato=kwargs['formato']
        )
