class MetaGestor(type):
    """
    Metaclase derivada de `type` que actúa como guardián del contrato CRUD.

    Al momento de definir una clase, verifica que implemente los cinco métodos
    públicos mínimos que todo gestor del sistema debe exponer:
        alta, baja, modificacion, listado, buscar

    Si alguno falta, la definición de la clase falla con un TypeError descriptivo,
    impidiendo instanciar un gestor incompleto.

    Ejemplo de uso:
        class GestionLibros(metaclass=MetaGestor):
            def alta(self, ...): ...
            def baja(self, ...): ...
            def modificacion(self, ...): ...
            def listado(self): ...
            def buscar(self, ...): ...
    """

    _METODOS_REQUERIDOS = frozenset({"alta", "baja", "modificacion", "listado", "buscar"})

    def __new__(mcs, nombre, bases, namespace):
        cls = super().__new__(mcs, nombre, bases, namespace)

        # Recolectar todos los métodos públicos disponibles (propios y heredados)
        metodos_disponibles = {
            name
            for klass in cls.__mro__
            for name, val in vars(klass).items()
            if callable(val) and not name.startswith("_")
        }

        faltantes = mcs._METODOS_REQUERIDOS - metodos_disponibles
        if faltantes:
            raise TypeError(
                f"La clase '{nombre}' no cumple el contrato MetaGestor. "
                f"Métodos faltantes: {sorted(faltantes)}"
            )

        return cls
