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

    # ── nombre ────────────────────────────────────────────────────────────────
    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self._nombre = value.strip()

    # ── apellido ──────────────────────────────────────────────────────────────
    @property
    def apellido(self) -> str:
        return self._apellido

    @apellido.setter
    def apellido(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("El apellido no puede estar vacío.")
        self._apellido = value.strip()

    # ── dni ───────────────────────────────────────────────────────────────────
    @property
    def dni(self) -> int:
        return self._dni

    @dni.setter
    def dni(self, value: int) -> None:
        if not isinstance(value, int) or value < 1:
            raise ValueError("El DNI debe ser un entero positivo.")
        self._dni = value

    # ── correo ────────────────────────────────────────────────────────────────
    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip() or "@" not in value:
            raise ValueError("El correo debe ser un email válido (debe contener '@').")
        self._correo = value.strip()

    def actualizar_notificacion(self, recurso):
        """
        Método del patrón Observer llamado por el Sujeto.
        """
        print(f"Notificacion enviada a: {self.correo}\nEl recurso '{recurso.titulo}' ya se encuentra disponible.")

    @abstractmethod
    def limite_prestamos(self) -> int:
        pass

    # ── representación ────────────────────────────────────────────────────────
    def __str__(self) -> str:
        return (
            f"  ID           : {self.id}\n"
            f"  Tipo         : {self.__class__.__name__}\n"
            f"  Nombre       : {self.nombre}\n"
            f"  Apellido     : {self.apellido}\n"
            f"  DNI          : {self.dni}\n"
            f"  Correo       : {self.correo}\n"
            f"  Registrado   : {self.fecha_creacion.strftime('%d/%m/%Y %H:%M')}"
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(id={self.id}, dni={self.dni}, nombre='{self.nombre}', apellido='{self.apellido}')"
        )


class Alumno(Usuario):
    def limite_prestamos(self) -> int:
        return 3


class Profesor(Usuario):
    def limite_prestamos(self) -> int:
        return 5