# TPF — Sistema de Gestión de Biblioteca Digital

Sistema desarrollado en Python utilizando **Programación Orientada a Objetos** como Trabajo Práctico Final de la materia. Permite administrar libros, usuarios y préstamos desde una interfaz de consola interactiva.

## Integrantes

- Miguel Miguez
- Rodrigo Podoba
- Milena Iñiguez
- Damián Larrascq Mechoso

---

## Estructura del proyecto

```
TPF-Biblioteca-Digital/
│
├── main.py                        # Punto de entrada. Menú principal de consola.
│
├── models/                        # Paquete: definición de entidades del dominio
│   ├── __init__.py                # Exporta todas las entidades y factories
│   ├── entidad_base.py            # Clase base abstracta con ID y fecha de creación
│   ├── libro.py                   # Entidad Libro legacy (usado por GestionLibros)
│   ├── recurso.py                 # Clase abstracta Recurso (Sujeto/Observer) + Libro y AudioLibro
│   ├── recurso_estados.py         # Patrón State: EstadoDisponible y EstadoPrestado
│   ├── recurso_factory.py         # Patrón Factory Method: LibroFactory y AudioLibroFactory
│   ├── usuario.py                 # Clase abstracta Usuario (Observer) + Alumno y Profesor
│   ├── usuario_factory.py         # Patrón Factory Method: AlumnoFactory y ProfesorFactory
│   └── prestamo.py                # Entidad Prestamo: asocia Usuario y Recurso
│
└── gestion/                       # Paquete: lógica de negocio / operaciones CRUD
    ├── __init__.py                # Exporta GestionLibros
    └── gestion_libros.py          # Alta, modificación, baja, listado y búsqueda de libros
```

---

## Jerarquía de clases

```
EntidadBase
    ├── Recurso  (abstracta — Sujeto/Observer)
    │   ├── Libro
    │   └── AudioLibro
    ├── Usuario  (abstracta — Observer)
    │   ├── Alumno
    │   └── Profesor
    └── Prestamo
```

| Clase               | Archivo                     | Responsabilidad                                                                                                                 |
| ------------------- | --------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `EntidadBase`       | `models/entidad_base.py`    | Clase padre de todas las entidades. Genera un ID auto-incremental y almacena la fecha de creación.                              |
| `Recurso`           | `models/recurso.py`         | Clase abstracta que actúa como **Sujeto** del patrón Observer. Administra su estado (disponible/prestado) y la lista de espera. |
| `Libro`             | `models/recurso.py`         | Recurso físico con ISBN y cantidad de páginas.                                                                                  |
| `AudioLibro`        | `models/recurso.py`         | Recurso digital con duración en minutos y formato.                                                                              |
| `EstadoRecurso`     | `models/recurso_estados.py` | Clase abstracta base del patrón **State** para los estados de un recurso.                                                       |
| `EstadoDisponible`  | `models/recurso_estados.py` | Estado concreto: permite préstamo y notifica observadores al volver a estar disponible.                                         |
| `EstadoPrestado`    | `models/recurso_estados.py` | Estado concreto: rechaza nuevos préstamos y permite devolución.                                                                 |
| `RecursoFactory`    | `models/recurso_factory.py` | Creador abstracto del patrón **Factory Method** para recursos.                                                                  |
| `LibroFactory`      | `models/recurso_factory.py` | Fábrica concreta que crea instancias de `Libro`.                                                                                |
| `AudioLibroFactory` | `models/recurso_factory.py` | Fábrica concreta que crea instancias de `AudioLibro`.                                                                           |
| `Usuario`           | `models/usuario.py`         | Clase abstracta que actúa como **Observer**. Define `limite_prestamos()` y el método de notificación.                           |
| `Alumno`            | `models/usuario.py`         | Usuario con límite de 3 préstamos simultáneos.                                                                                  |
| `Profesor`          | `models/usuario.py`         | Usuario con límite de 5 préstamos simultáneos.                                                                                  |
| `UsuarioFactory`    | `models/usuario_factory.py` | Creador abstracto del patrón **Factory Method** para usuarios.                                                                  |
| `AlumnoFactory`     | `models/usuario_factory.py` | Fábrica concreta que crea instancias de `Alumno`.                                                                               |
| `ProfesorFactory`   | `models/usuario_factory.py` | Fábrica concreta que crea instancias de `Profesor`.                                                                             |
| `Prestamo`          | `models/prestamo.py`        | Asocia un `Usuario` con un `Recurso`. Registra fecha de préstamo y permite registrar la devolución.                             |
| `GestionLibros`     | `gestion/gestion_libros.py` | Gestiona la colección de libros en memoria: alta, modificación, baja, listado y búsqueda.                                       |

---

## Patrones de diseño aplicados

### Observer — Lista de espera de recursos

`Recurso` actúa como **Sujeto**: mantiene una lista de `Usuario`s que se anotaron en espera. Cuando un recurso es devuelto y su estado cambia a `EstadoDisponible`, llama a `notificar_observadores()`, que recorre la lista y ejecuta `actualizar_notificacion()` en cada `Usuario`, simulando el envío de un correo.

```
Recurso (Sujeto)  ──notifica──▶  Usuario (Observer)
    │                                │
    ▼                                ▼
agregar_observador()         actualizar_notificacion()
remover_observador()
notificar_observadores()
```

### State — Estados de un recurso

El comportamiento de préstamo/devolución de `Recurso` depende del estado actual. En lugar de condicionales dispersos, cada estado encapsula su propia lógica:

| Estado             | `prestar()`                            | `devolver()`                               |
| ------------------ | -------------------------------------- | ------------------------------------------ |
| `EstadoDisponible` | Cambia a `EstadoPrestado` → `True`     | Informa que ya estaba disponible → `False` |
| `EstadoPrestado`   | Informa que ya está prestado → `False` | Cambia a `EstadoDisponible` → `True`       |

### Factory Method — Creación de entidades

Se definieron jerarquías de factories independientes para recursos y usuarios, desacoplando la lógica de creación del resto del sistema:

- `LibroFactory` / `AudioLibroFactory` → crean subclases de `Recurso`
- `AlumnoFactory` / `ProfesorFactory` → crean subclases de `Usuario`

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

Este patrón sigue el principio de **responsabilidad única (SRP)** y facilita incorporar nuevas entidades sin modificar código existente.

---

### 2. Clase base `EntidadBase`

Se creó una clase `EntidadBase` de la que heredan todas las entidades del sistema. Centraliza dos responsabilidades comunes:

- **ID auto-incremental:** evita que cada clase deba implementar su propio contador.
- **Fecha de creación:** registro automático sin intervención del usuario.

Todas las entidades (`Recurso`, `Usuario`, `Prestamo`) reutilizan estas propiedades sin duplicar código.

---

### 3. Clase abstracta `Recurso` con subtipos

En lugar de mantener un único modelo `Libro`, se introdujo `Recurso` como clase abstracta de la que heredan `Libro` y `AudioLibro`. Esto permite:

- Tratar todos los recursos de forma polimórfica en préstamos y estados.
- Agregar nuevos tipos de recursos (ej. `Revista`, `Podcast`) sin modificar la lógica de préstamo.
- Centralizar la lógica de Observer y State en la clase base.

---

### 4. Clase abstracta `Usuario` con subtipos

`Usuario` define el contrato del Observer (`actualizar_notificacion`) y delega en cada subtipo la política de `limite_prestamos()`. `Alumno` tiene límite 3 y `Profesor` límite 5, sin condicionales externos.

---

### 5. Validación con `@property` en `Libro`

Los atributos de `Libro` se exponen mediante `@property` con sus respectivos `@setter`. Esto permite:

- Validar los datos tanto en la construcción (`__init__`) como en una modificación posterior (`setattr` desde `GestionLibros.modificacion()`).
- Garantizar invariantes del dominio: título no vacío, año e ISBN positivos, etc.
- Mantener los atributos internos privados (`_titulo`, `_isbn`, etc.) sin exponer la implementación.

---

### 6. Método `modificacion()` con `**campos`

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
| Gestión de Préstamos | `Prestamo(EntidadBase)` / `GestionPrestamos` | Pendiente |
