from typing import List, Optional

from models.libro import Libro
from gestion.metaclases import MetaGestor
from gestion.decoradores import validar_cadenas


class GestionLibros(metaclass=MetaGestor):
    """Gestiona el ciclo de vida de los libros: alta, modificación, baja y listado."""

    def __init__(self):
        self._libros: List[Libro] = []

    # ── consultas internas ────────────────────────────────────────────────────
    def _buscar_por_id(self, id: int) -> Optional[Libro]:
        return next((l for l in self._libros if l.id == id), None)

    def _buscar_por_isbn(self, isbn: str) -> Optional[Libro]:
        return next((l for l in self._libros if l.isbn == isbn), None)

    # ── operaciones públicas ──────────────────────────────────────────────────
    @validar_cadenas
    def alta(
        self,
        titulo: str,
        autor: str,
        isbn: str,
        anio_publicacion: int,
        cantidad_paginas: int,
    ) -> Libro:
        """Registra un nuevo libro. Lanza ValueError si el ISBN ya existe."""
        if self._buscar_por_isbn(isbn):
            raise ValueError(f"Ya existe un libro con el ISBN '{isbn}'.")
        libro = Libro(titulo, autor, isbn, anio_publicacion, cantidad_paginas)
        self._libros.append(libro)
        return libro

    def modificacion(self, id: int, **campos) -> Libro:
        """Modifica campos de un libro existente identificado por su ID.

        Campos aceptados: titulo, autor, isbn, anio_publicacion, cantidad_paginas.
        Lanza ValueError si el ID no existe o si el nuevo ISBN ya pertenece a otro libro.
        """
        libro = self._buscar_por_id(id)
        if libro is None:
            raise ValueError(f"No se encontró ningún libro con ID {id}.")

        # Verificar colisión de ISBN antes de aplicar cambios
        nuevo_isbn = campos.get("isbn")
        if nuevo_isbn and nuevo_isbn != libro.isbn and self._buscar_por_isbn(nuevo_isbn):
            raise ValueError(f"El ISBN '{nuevo_isbn}' ya está en uso por otro libro.")

        campos_validos = {"titulo", "autor", "isbn", "anio_publicacion", "cantidad_paginas"}
        for campo, valor in campos.items():
            if campo not in campos_validos:
                raise ValueError(f"Campo desconocido: '{campo}'.")
            setattr(libro, campo, valor)

        return libro

    def baja(self, id: int) -> Libro:
        """Elimina el libro con el ID indicado y lo retorna. Lanza ValueError si no existe."""
        libro = self._buscar_por_id(id)
        if libro is None:
            raise ValueError(f"No se encontró ningún libro con ID {id}.")
        self._libros.remove(libro)
        return libro

    def listado(self) -> List[Libro]:
        """Retorna una copia de la lista de libros registrados."""
        return list(self._libros)

    @validar_cadenas
    def buscar(self, termino: str) -> List[Libro]:
        """Búsqueda parcial (case-insensitive) por título, autor o ISBN."""
        termino = termino.lower()
        return [
            l for l in self._libros
            if termino in l.titulo.lower()
            or termino in l.autor.lower()
            or termino in l.isbn.lower()
        ]

    def __len__(self) -> int:
        return len(self._libros)
