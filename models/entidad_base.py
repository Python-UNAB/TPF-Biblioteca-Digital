from datetime import datetime


class EntidadBase:
    """Clase base para todas las entidades del sistema."""

    _id_counter: int = 0

    def __init__(self):
        EntidadBase._id_counter += 1
        self._id: int = EntidadBase._id_counter
        self._fecha_creacion: datetime = datetime.now()

    @property
    def id(self) -> int:
        return self._id

    @property
    def fecha_creacion(self) -> datetime:
        return self._fecha_creacion

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self._id})"
