from typing import List, Optional

from models import Usuario, AlumnoFactory, ProfesorFactory
from gestion.metaclases import MetaGestor
from gestion.decoradores import validar_cadenas


class GestionUsuarios(metaclass=MetaGestor):
    """Gestiona el ciclo de vida de los usuarios (Alumnos y Profesores): alta, modificación, baja, listado y búsqueda."""

    def __init__(self):
        self._usuarios: List[Usuario] = []
        self._factories = {
            "alumno": AlumnoFactory(),
            "profesor": ProfesorFactory(),
        }

    # ── consultas internas ────────────────────────────────────────────────────
    def _buscar_por_id(self, id: int) -> Optional[Usuario]:
        return next((u for u in self._usuarios if u.id == id), None)

    def _buscar_por_dni(self, dni: int) -> Optional[Usuario]:
        return next((u for u in self._usuarios if u.dni == dni), None)

    # ── operaciones públicas ──────────────────────────────────────────────────
    @validar_cadenas
    def alta(
        self,
        tipo: str,
        nombre: str,
        apellido: str,
        dni: int,
        correo: str,
    ) -> Usuario:
        """Registra un nuevo usuario (Alumno o Profesor) utilizando su respectiva fábrica.
        
        Lanza ValueError si el tipo de usuario es inválido o si el DNI ya existe.
        """
        tipo_normalizado = tipo.lower().strip()
        if tipo_normalizado not in self._factories:
            raise ValueError(
                f"Tipo de usuario inválido: '{tipo}'. Debe ser 'alumno' o 'profesor'."
            )

        if self._buscar_por_dni(dni):
            raise ValueError(f"Ya existe un usuario con el DNI {dni}.")

        factory = self._factories[tipo_normalizado]
        usuario = factory.crear_usuario(
            nombre=nombre,
            apellido=apellido,
            dni=dni,
            correo=correo,
        )
        self._usuarios.append(usuario)
        return usuario

    def modificacion(self, id: int, **campos) -> Usuario:
        """Modifica campos de un usuario existente identificado por su ID.

        Campos aceptados: nombre, apellido, dni, correo.
        Lanza ValueError si el ID no existe o si el nuevo DNI ya pertenece a otro usuario.
        """
        usuario = self._buscar_por_id(id)
        if usuario is None:
            raise ValueError(f"No se encontró ningún usuario con ID {id}.")

        # Verificar colisión de DNI si se intenta modificar
        nuevo_dni = campos.get("dni")
        if nuevo_dni is not None:
            if nuevo_dni != usuario.dni and self._buscar_por_dni(nuevo_dni):
                raise ValueError(f"El DNI {nuevo_dni} ya está en uso por otro usuario.")

        campos_validos = {"nombre", "apellido", "dni", "correo"}
        for campo, valor in campos.items():
            if campo not in campos_validos:
                raise ValueError(f"Campo desconocido: '{campo}'.")
            setattr(usuario, campo, valor)

        return usuario

    def baja(self, id: int) -> Usuario:
        """Elimina al usuario con el ID indicado y lo retorna. Lanza ValueError si no existe."""
        usuario = self._buscar_por_id(id)
        if usuario is None:
            raise ValueError(f"No se encontró ningún usuario con ID {id}.")
        self._usuarios.remove(usuario)
        return usuario

    def listado(self) -> List[Usuario]:
        """Retorna una copia de la lista de usuarios registrados."""
        return list(self._usuarios)

    @validar_cadenas
    def buscar(self, termino: str) -> List[Usuario]:
        """Búsqueda parcial (case-insensitive) por nombre, apellido, DNI o correo."""
        termino = termino.lower()
        return [
            u for u in self._usuarios
            if termino in u.nombre.lower()
            or termino in u.apellido.lower()
            or termino in str(u.dni)
            or termino in u.correo.lower()
        ]

    def __len__(self) -> int:
        return len(self._usuarios)
