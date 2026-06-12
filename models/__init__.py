from models.entidad_base import EntidadBase
from models.libro import Libro
from .recurso import Recurso, Libro, AudioLibro
from .recurso_estados import EstadoRecurso, EstadoDisponible, EstadoPrestado
from

__all__ = ["EntidadBase", "Libro"]
