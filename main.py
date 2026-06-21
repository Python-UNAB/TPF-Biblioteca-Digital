"""
main.py — Punto de entrada del Sistema de Gestión de Biblioteca Digital.

Importa los módulos del paquete `models` y `gestion` para exponer
las operaciones de Gestión de Libros a través de un menú de consola.
"""

from models import Libro  # noqa: F401  (disponible para uso futuro / herencia)
from gestion import GestionLibros, GestionUsuarios


# ── helpers de entrada ────────────────────────────────────────────────────────

def _leer_str(prompt: str) -> str:
    valor = input(prompt).strip()
    if not valor:
        raise ValueError("El campo no puede estar vacío.")
    return valor


def _leer_int(prompt: str) -> int:
    try:
        return int(input(prompt).strip())
    except ValueError:
        raise ValueError("Debe ingresar un número entero válido.")


# ── submenú libros ─────────────────────────────────────────────────────────────

def _menu_libros(gestion: GestionLibros) -> None:
    opciones = (
        "\n── Gestión de Libros ──────────────────────"
        "\n  1. Alta de libro"
        "\n  2. Modificar libro"
        "\n  3. Baja de libro"
        "\n  4. Listar libros"
        "\n  5. Buscar libro"
        "\n  0. Volver al menú principal"
        "\n────────────────────────────────────────────"
    )

    while True:
        print(opciones)
        opcion = input("Seleccioná una opción: ").strip()

        if opcion == "1":
            _alta_libro(gestion)
        elif opcion == "2":
            _modificar_libro(gestion)
        elif opcion == "3":
            _baja_libro(gestion)
        elif opcion == "4":
            _listar_libros(gestion)
        elif opcion == "5":
            _buscar_libro(gestion)
        elif opcion == "0":
            break
        else:
            print("[!] Opción inválida. Intentá de nuevo.")


def _alta_libro(gestion: GestionLibros) -> None:
    print("\n── Alta de Libro ──")
    try:
        titulo = _leer_str("  Título          : ")
        autor = _leer_str("  Autor           : ")
        isbn = _leer_str("  ISBN            : ")
        anio = _leer_int("  Año publicación : ")
        paginas = _leer_int("  Cantidad páginas: ")
        libro = gestion.alta(titulo, autor, isbn, anio, paginas)
        print(f"\n[✓] Libro registrado exitosamente:\n{libro}")
    except ValueError as e:
        print(f"[!] Error: {e}")


def _modificar_libro(gestion: GestionLibros) -> None:
    print("\n── Modificación de Libro ──")
    if not gestion.listado():
        print("[!] No hay libros registrados.")
        return
    try:
        id_libro = _leer_int("  ID del libro a modificar: ")
        print("  (Dejá en blanco los campos que no querés cambiar)")

        campos: dict = {}
        for campo, label, tipo in [
            ("titulo",           "Nuevo título",           str),
            ("autor",            "Nuevo autor",            str),
            ("isbn",             "Nuevo ISBN",             str),
            ("anio_publicacion", "Nuevo año publicación",  int),
            ("cantidad_paginas", "Nueva cantidad páginas", int),
        ]:
            raw = input(f"  {label}: ").strip()
            if raw:
                campos[campo] = tipo(raw)

        if not campos:
            print("[!] No se realizaron cambios.")
            return

        libro = gestion.modificacion(id_libro, **campos)
        print(f"\n[✓] Libro actualizado:\n{libro}")
    except ValueError as e:
        print(f"[!] Error: {e}")


def _baja_libro(gestion: GestionLibros) -> None:
    print("\n── Baja de Libro ──")
    if not gestion.listado():
        print("[!] No hay libros registrados.")
        return
    try:
        id_libro = _leer_int("  ID del libro a eliminar: ")
        libro = gestion.baja(id_libro)
        print(f"[✓] Libro eliminado: {repr(libro)}")
    except ValueError as e:
        print(f"[!] Error: {e}")


def _listar_libros(gestion: GestionLibros) -> None:
    libros = gestion.listado()
    if not libros:
        print("\n[!] No hay libros registrados.")
        return
    print(f"\n── Listado de Libros ({len(libros)} registros) ──")
    for libro in libros:
        print(f"\n{libro}\n  {'─' * 40}")


def _buscar_libro(gestion: GestionLibros) -> None:
    print("\n── Búsqueda de Libro ──")
    try:
        termino = _leer_str("  Término de búsqueda (título / autor / ISBN): ")
        resultados = gestion.buscar(termino)
        if not resultados:
            print("[!] No se encontraron coincidencias.")
        else:
            print(f"\n  {len(resultados)} resultado(s):")
            for libro in resultados:
                print(f"\n{libro}\n  {'─' * 40}")
    except ValueError as e:
        print(f"[!] Error: {e}")


# ── submenú usuarios ───────────────────────────────────────────────────────────

def _menu_usuarios(gestion: GestionUsuarios) -> None:
    opciones = (
        "\n── Gestión de Usuarios ────────────────────"
        "\n  1. Alta de usuario"
        "\n  2. Modificar usuario"
        "\n  3. Baja de usuario"
        "\n  4. Listar usuarios"
        "\n  5. Buscar usuario"
        "\n  0. Volver al menú principal"
        "\n────────────────────────────────────────────"
    )

    while True:
        print(opciones)
        opcion = input("Seleccioná una opción: ").strip()

        if opcion == "1":
            _alta_usuario(gestion)
        elif opcion == "2":
            _modificar_usuario(gestion)
        elif opcion == "3":
            _baja_usuario(gestion)
        elif opcion == "4":
            _listar_usuarios(gestion)
        elif opcion == "5":
            _buscar_usuario(gestion)
        elif opcion == "0":
            break
        else:
            print("[!] Opción inválida. Intentá de nuevo.")


def _alta_usuario(gestion: GestionUsuarios) -> None:
    print("\n── Alta de Usuario ──")
    try:
        tipo = _leer_str("  Tipo (alumno / profesor): ").strip().lower()
        if tipo not in ["alumno", "profesor"]:
            raise ValueError("El tipo debe ser 'alumno' o 'profesor'.")
        
        nombre = _leer_str("  Nombre          : ")
        apellido = _leer_str("  Apellido        : ")
        dni = _leer_int("  DNI             : ")
        correo = _leer_str("  Correo          : ")
        
        usuario = gestion.alta(tipo, nombre, apellido, dni, correo)
        print(f"\n[✓] Usuario registrado exitosamente:\n{usuario}")
    except ValueError as e:
        print(f"[!] Error: {e}")


def _modificar_usuario(gestion: GestionUsuarios) -> None:
    print("\n── Modificación de Usuario ──")
    if not gestion.listado():
        print("[!] No hay usuarios registrados.")
        return
    try:
        id_usuario = _leer_int("  ID del usuario a modificar: ")
        print("  (Dejá en blanco los campos que no querés cambiar)")

        campos: dict = {}
        for campo, label, tipo in [
            ("nombre",   "Nuevo nombre",   str),
            ("apellido", "Nuevo apellido", str),
            ("dni",      "Nuevo DNI",      int),
            ("correo",   "Nuevo correo",   str),
        ]:
            raw = input(f"  {label}: ").strip()
            if raw:
                campos[campo] = tipo(raw)

        if not campos:
            print("[!] No se realizaron cambios.")
            return

        usuario = gestion.modificacion(id_usuario, **campos)
        print(f"\n[✓] Usuario actualizado:\n{usuario}")
    except ValueError as e:
        print(f"[!] Error: {e}")


def _baja_usuario(gestion: GestionUsuarios) -> None:
    print("\n── Baja de Usuario ──")
    if not gestion.listado():
        print("[!] No hay usuarios registrados.")
        return
    try:
        id_usuario = _leer_int("  ID del usuario a eliminar: ")
        usuario = gestion.baja(id_usuario)
        print(f"[✓] Usuario eliminado: {repr(usuario)}")
    except ValueError as e:
        print(f"[!] Error: {e}")


def _listar_usuarios(gestion: GestionUsuarios) -> None:
    usuarios = gestion.listado()
    if not usuarios:
        print("\n[!] No hay usuarios registrados.")
        return
    print(f"\n── Listado de Usuarios ({len(usuarios)} registros) ──")
    for usuario in usuarios:
        print(f"\n{usuario}\n  {'─' * 40}")


def _buscar_usuario(gestion: GestionUsuarios) -> None:
    print("\n── Búsqueda de Usuario ──")
    try:
        termino = _leer_str("  Término de búsqueda (nombre / apellido / DNI / correo): ")
        resultados = gestion.buscar(termino)
        if not resultados:
            print("[!] No se encontraron coincidencias.")
        else:
            print(f"\n  {len(resultados)} resultado(s):")
            for usuario in resultados:
                print(f"\n{usuario}\n  {'─' * 40}")
    except ValueError as e:
        print(f"[!] Error: {e}")


# ── menú principal ─────────────────────────────────────────────────────────────

def main() -> None:
    gestion_libros = GestionLibros()
    gestion_usuarios = GestionUsuarios()

    menu_principal = (
        "\n╔══════════════════════════════════════════╗"
        "\n║   Sistema de Biblioteca Digital          ║"
        "\n╠══════════════════════════════════════════╣"
        "\n║  1. Gestión de Libros                    ║"
        "\n║  2. Gestión de Usuarios                  ║"
        "\n║  0. Salir                                ║"
        "\n╚══════════════════════════════════════════╝"
    )

    while True:
        print(menu_principal)
        opcion = input("Seleccioná una opción: ").strip()

        if opcion == "1":
            _menu_libros(gestion_libros)
        elif opcion == "2":
            _menu_usuarios(gestion_usuarios)
        elif opcion == "0":
            print("\nHasta luego.\n")
            break
        else:
            print("[!] Opción inválida. Intentá de nuevo.")


if __name__ == "__main__":
    main()
