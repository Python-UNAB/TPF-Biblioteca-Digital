from abc import abstractmethod
from models.entidad_base import EntidadBase
from models.recurso_estados import EstadoDisponible


class Recurso(EntidadBase):
    """
    Clase abstracta. Actua como 'Sujeto'
    """

    def __init__(self, titulo: str, autor: str, anio: int):
        super().__init__()
        self.titulo = titulo
        self.autor = autor
        self.anio = anio
        self._estado = EstadoDisponible()
        self._observadores = [] # Lista de usuarios

    def set_estado(self, nuevo_estado):
        self._estado = nuevo_estado

        if isinstance(nuevo_estado, EstadoDisponible):
            self.notificar_observadores()

    def intentar_prestar(self) -> bool:
        return self._estado.prestar(self)

    def intentar_devolver(self) -> bool:
        return self._estado.devolver(self)

    # Metodos Observer

    def agregar_observador(self, usuario):
        if usuario not in self._observadores:
            self._observadores.append(usuario)
            print(f"'{usuario.nombre} {usuario.apellido}' se anoto en la lista de espera.")

    def remover_observador(self, usuario):
        if usuario in self._observadores:
            self._observadores.remove(usuario)

    def notificar_observadores(self):
        if self._observadores:
            print(f"El recurso '{self.titulo}' se libero. Notificando lista de espera.")

            for usuario in list(self._observadores):
                usuario.actualizar_notificacion(self)
                self.remover_observador(usuario)

    @abstractmethod
    def obtener_detalles(self) -> str:
        pass


class Libro(Recurso):
    def __init__(self, titulo: str, autor: str, anio: int, isbn: str, paginas: int):
        super().__init__(titulo, autor, anio)
        self.isbn = isbn
        self.paginas = paginas

    def obtener_detalles(self) -> str:
        return f"[Libro Fisico] ID: {self.id} | {self.titulo} - {self.autor} (ISBN: {self.isbn})"


class AudioLibro(Recurso):
    def __init__(self, titulo: str, autor: str, anio: int, duracion_minutos: int, formato: str):
        super().__init__(titulo, autor, anio)
        self.duracion_minutos = duracion_minutos
        self.formato = formato

    def obtener_detalles(self) -> str:
        return f"[AudioLibro] ID: {self.id} | {self.titulo} - {self.autor} ({self.duracion_minutos} min | {self.formato})"