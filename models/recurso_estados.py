from abc import ABC, abstractmethod


class EstadoRecurso(ABC):
    """
    Clase base abstracta para el patrón State.
    """

    @abstractmethod
    def prestar(self, recurso) -> bool:
        pass

    @abstractmethod
    def devolver(self, recurso) -> bool:
        pass


class EstadoDisponible(EstadoRecurso):

    def prestar(self, recurso) -> bool:
        print(f"'{recurso.titulo}' ha sido prestado con éxito.")
        recurso.set_estado(EstadoPrestado())
        return True

    def devolver(self, recurso) -> bool:
        print(f"'{recurso.titulo}' ya estaba disponible.")
        return False


class EstadoPrestado(EstadoRecurso):
    def prestar(self, recurso) -> bool:
        print(f"Error: '{recurso.titulo}' ya se encuentra prestado actualmente.")
        return False

    def devolver(self, recurso) -> bool:
        print(f"'{recurso.titulo}' fue devuelto correctamente.")
        recurso.set_estado(EstadoDisponible())
        return True