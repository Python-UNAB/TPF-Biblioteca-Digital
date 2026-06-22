from typing import List, Optional

from models import Recurso, LibroFactory, AudioLibroFactory
from gestion.metaclases import MetaGestor
from gestion.decoradores import validar_cadenas


class GestionRecursos(metaclass=MetaGestor):
    """Gestiona la colección de recursos (Libros y AudioLibros) disponibles para préstamo."""

    def __init__(self):
        self._recursos: List[Recurso] = []
        self._factories = {
            "libro": LibroFactory(),
            "audiolibro": AudioLibroFactory(),
        }

    # ── consultas internas ─────────────────────────────────────────────────────
    def _buscar_por_id(self, id: int) -> Optional[Recurso]:
        return next((r for r in self._recursos if r.id == id), None)

    # ── operaciones públicas ───────────────────────────────────────────────────
    @validar_cadenas
    def alta(self, tipo: str, **kwargs) -> Recurso:
        """Registra un nuevo recurso usando la fábrica correspondiente ('libro' o 'audiolibro')."""
        tipo_normalizado = tipo.lower().strip()
        if tipo_normalizado not in self._factories:
            raise ValueError(f"Tipo inválido: '{tipo}'. Debe ser 'libro' o 'audiolibro'.")
        recurso = self._factories[tipo_normalizado].crear_recurso(**kwargs)
        self._recursos.append(recurso)
        return recurso

    def modificacion(self, id: int, **campos) -> Recurso:
        """Modifica campos de un recurso existente identificado por su ID."""
        recurso = self._buscar_por_id(id)
        if recurso is None:
            raise ValueError(f"No se encontró ningún recurso con ID {id}.")
        campos_validos = {"titulo", "autor", "anio", "isbn", "paginas", "duracion_minutos", "formato"}
        for campo, valor in campos.items():
            if campo not in campos_validos:
                raise ValueError(f"Campo desconocido: '{campo}'.")
            setattr(recurso, campo, valor)
        return recurso

    def baja(self, id: int) -> Recurso:
        """Elimina el recurso con el ID indicado. Lanza ValueError si no existe."""
        recurso = self._buscar_por_id(id)
        if recurso is None:
            raise ValueError(f"No se encontró ningún recurso con ID {id}.")
        self._recursos.remove(recurso)
        return recurso

    def listado(self) -> List[Recurso]:
        """Retorna una copia de la lista de recursos registrados."""
        return list(self._recursos)

    @validar_cadenas
    def buscar(self, termino: str) -> List[Recurso]:
        """Búsqueda parcial (case-insensitive) por título o autor."""
        termino_lower = termino.lower()
        return [
            r for r in self._recursos
            if termino_lower in r.titulo.lower() or termino_lower in r.autor.lower()
        ]

    def obtener_por_id(self, id: int) -> Optional[Recurso]:
        """Retorna el recurso con el ID dado, o None si no existe."""
        return self._buscar_por_id(id)

    def __len__(self) -> int:
        return len(self._recursos)
