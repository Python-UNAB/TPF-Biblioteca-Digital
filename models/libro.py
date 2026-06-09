from models.entidad_base import EntidadBase


class Libro(EntidadBase):
    """Representa un libro dentro del sistema de biblioteca digital."""

    def __init__(
        self,
        titulo: str,
        autor: str,
        isbn: str,
        anio_publicacion: int,
        cantidad_paginas: int,
    ):
        super().__init__()
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.anio_publicacion = anio_publicacion
        self.cantidad_paginas = cantidad_paginas

    # ── titulo ────────────────────────────────────────────────────────────────
    @property
    def titulo(self) -> str:
        return self._titulo

    @titulo.setter
    def titulo(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("El título no puede estar vacío.")
        self._titulo = value.strip()

    # ── autor ─────────────────────────────────────────────────────────────────
    @property
    def autor(self) -> str:
        return self._autor

    @autor.setter
    def autor(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("El autor no puede estar vacío.")
        self._autor = value.strip()

    # ── isbn ──────────────────────────────────────────────────────────────────
    @property
    def isbn(self) -> str:
        return self._isbn

    @isbn.setter
    def isbn(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("El ISBN no puede estar vacío.")
        self._isbn = value.strip()

    # ── anio_publicacion ──────────────────────────────────────────────────────
    @property
    def anio_publicacion(self) -> int:
        return self._anio_publicacion

    @anio_publicacion.setter
    def anio_publicacion(self, value: int) -> None:
        if not isinstance(value, int) or value < 1:
            raise ValueError("El año de publicación debe ser un entero positivo.")
        self._anio_publicacion = value

    # ── cantidad_paginas ──────────────────────────────────────────────────────
    @property
    def cantidad_paginas(self) -> int:
        return self._cantidad_paginas

    @cantidad_paginas.setter
    def cantidad_paginas(self, value: int) -> None:
        if not isinstance(value, int) or value < 1:
            raise ValueError("La cantidad de páginas debe ser un entero positivo.")
        self._cantidad_paginas = value

    # ── representación ────────────────────────────────────────────────────────
    def __str__(self) -> str:
        return (
            f"  ID           : {self.id}\n"
            f"  Título       : {self.titulo}\n"
            f"  Autor        : {self.autor}\n"
            f"  ISBN         : {self.isbn}\n"
            f"  Año          : {self.anio_publicacion}\n"
            f"  Páginas      : {self.cantidad_paginas}\n"
            f"  Registrado   : {self.fecha_creacion.strftime('%d/%m/%Y %H:%M')}"
        )

    def __repr__(self) -> str:
        return (
            f"Libro(id={self.id}, isbn='{self.isbn}', titulo='{self.titulo}')"
        )
