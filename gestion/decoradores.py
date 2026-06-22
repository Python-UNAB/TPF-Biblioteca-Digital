import inspect
import functools


def validar_cadenas(func):
    """
    Decorador propio que valida, antes de ejecutar el método decorado,
    que todos los parámetros anotados como `str` no estén vacíos
    ni contengan únicamente espacios en blanco.

    Ejemplo de uso:
        @validar_cadenas
        def alta(self, titulo: str, autor: str, anio: int): ...
    """
    sig = inspect.signature(func)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()

        for nombre, valor in bound.arguments.items():
            param = sig.parameters[nombre]
            if param.annotation is str and isinstance(valor, str) and not valor.strip():
                raise ValueError(
                    f"El parámetro '{nombre}' no puede estar vacío ni contener solo espacios."
                )

        return func(*args, **kwargs)

    return wrapper
