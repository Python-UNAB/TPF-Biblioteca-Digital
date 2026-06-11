# TPF — Sistema de Gestión de Biblioteca Digital

Sistema desarrollado en Python utilizando **Programación Orientada a Objetos** como Trabajo Práctico Final de la materia. Permite administrar libros, usuarios y préstamos desde una interfaz de consola interactiva.

## Integrantes

- Miguel Miguez
- Rodrigo Podoba
- Milena Iñiguez

---

## Estructura del proyecto

```
TPF-Biblioteca-Digital/
│
├── main.py                        # Punto de entrada. Menú principal de consola.
│
├── models/                        # Paquete: definición de entidades del dominio
│   ├── __init__.py                # Exporta EntidadBase y Libro
│   ├── entidad_base.py            # Clase base abstracta con ID y fecha de creación
│   └── libro.py                   # Entidad Libro, hereda de EntidadBase
│
└── gestion/                       # Paquete: lógica de negocio / operaciones CRUD
    ├── __init__.py                # Exporta GestionLibros
    └── gestion_libros.py          # Alta, modificación, baja, listado y búsqueda
```

---

## Jerarquía de clases

```
EntidadBase
    └── Libro
```

| Clase           | Archivo                     | Responsabilidad                                                                                                                 |
| --------------- | --------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `EntidadBase`   | `models/entidad_base.py`    | Clase padre de todas las entidades. Genera un ID auto-incremental y almacena la fecha de creación.                              |
| `Libro`         | `models/libro.py`           | Hereda de `EntidadBase`. Contiene título, autor, ISBN, año de publicación y cantidad de páginas con validación por `@property`. |
| `GestionLibros` | `gestion/gestion_libros.py` | Gestiona la colección de libros en memoria: alta, modificación, baja, listado y búsqueda.                                       |

---

## Cómo ejecutar

```bash
python main.py
```

Requiere **Python 3.8+**. No tiene dependencias externas.

---

## Toma de decisiones sobre la arquitectura

### 1. Separación en paquetes `models/` y `gestion/`

Se decidió dividir el proyecto en dos paquetes con responsabilidades bien diferenciadas:

- **`models/`** contiene únicamente la definición de las entidades del dominio (qué _son_ los objetos). No incluye lógica de negocio ni acceso a datos.
- **`gestion/`** contiene la lógica operacional (qué _se hace_ con los objetos). Cada módulo de gestión conoce su modelo correspondiente, pero el modelo no conoce al gestor.

Este patrón sigue el principio de **responsabilidad única (SRP)** y facilita incorporar nuevas entidades (ej. `Usuario`, `Prestamo`) sin modificar código existente.

---

### 2. Clase base `EntidadBase`

Se creó una clase `EntidadBase` de la que heredan todas las entidades del sistema. Centraliza dos responsabilidades comunes:

- **ID auto-incremental:** evita que cada clase deba implementar su propio contador.
- **Fecha de creación:** registro automático sin intervención del usuario.

Esto anticipa la incorporación de `Usuario` y `Prestamo`, que también necesitarán estas propiedades, sin duplicar código.

---

### 3. Validación con `@property` en `Libro`

Los atributos de `Libro` se exponen mediante `@property` con sus respectivos `@setter`. Esto permite:

- Validar los datos tanto en la construcción (`__init__`) como en una modificación posterior (`setattr` desde `GestionLibros.modificacion()`).
- Garantizar invariantes del dominio: título no vacío, año e ISBN positivos, etc.
- Mantener los atributos internos privados (`_titulo`, `_isbn`, etc.) sin exponer la implementación.

---

### 4. Método `modificacion()` con `**campos`

En lugar de definir un método con parámetros fijos para cada campo modificable, `GestionLibros.modificacion()` recibe un diccionario de campos (`**kwargs`). Esto:

- Permite actualizar uno o varios campos en una sola llamada.
- Reutiliza la validación ya implementada en los `@setter` de `Libro` mediante `setattr`.
- Facilita extender el modelo con nuevos campos sin cambiar la firma del método.

---

### 5. Control de unicidad por ISBN

`GestionLibros.alta()` y `GestionLibros.modificacion()` verifican que no existan dos libros con el mismo ISBN antes de confirmar la operación. El ISBN es el identificador natural de un libro en el dominio real, por lo que duplicarlo sería un error de negocio independientemente del ID interno.

---

### 6. `main.py` como capa de presentación pura

`main.py` únicamente maneja la interacción con el usuario (entrada/salida por consola). No contiene lógica de negocio ni manipula estructuras de datos directamente. Delega todas las operaciones a `GestionLibros`, respetando la separación entre **presentación** y **lógica de negocio**.

---

## Módulos pendientes (próximas iteraciones)

| Módulo               | Clase principal                              | Estado    |
| -------------------- | -------------------------------------------- | --------- |
| Gestión de Usuarios  | `Usuario(EntidadBase)` / `GestionUsuarios`   | Pendiente |
| Gestión de Préstamos | `Prestamo(EntidadBase)` / `GestionPrestamos` | Pendiente |
