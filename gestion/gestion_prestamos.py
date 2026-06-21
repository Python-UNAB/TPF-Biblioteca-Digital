from models.prestamo import Prestamo


class GestionPrestamo:
    """
    Clase encargada de controlar el ciclo de vida de los préstamos (Composición).
    """

    def __init__(self):
        # Las listas contienen los objetos Prestamo y su ciclo de vida depende de este gestor
        self._prestamos_activos = []
        self._historial_prestamos = []

    def registrar_prestamo(self, usuario, recurso):
        """
        Registra un préstamo validando los límites del usuario y el estado del recurso.
        Si el recurso está ocupado, ofrece suscribir al usuario a la lista de espera
        """

        # 1. Validar límite de préstamos
        prestamos_actuales = sum(1 for prestamo in self._prestamos_activos if prestamo.usuario.dni == usuario.dni)
        if prestamos_actuales >= usuario.limite_prestamos():
            print(f"\n{usuario.nombre} {usuario.apellido} ya alcanzó su límite máximo de préstamos ({usuario.limite_prestamos()}).")
            return None

        # 2. Intentar cambiar el estado del recurso
        # Si el estado actual es Disponible, cambiará a Prestado y devuelve True
        if recurso.intentar_prestar():
            nuevo_prestamo = Prestamo(usuario, recurso)
            self._prestamos_activos.append(nuevo_prestamo)
            print(f"Préstamo ID {nuevo_prestamo.id} registrado con éxito.")
            return nuevo_prestamo

        else:
            # 3. Si el libro ya estaba prestado (State), se agrega el usuario a la lista de espera (Observer)
            print(f"'{recurso.titulo}' no está disponible.")
            recurso.agregar_observador(usuario)
            return None

    def registrar_devolucion(self, recurso):
        """
        Procesa la devolución de un recurso, finaliza el objeto préstamo
        y activa las alertas automáticas si hay usuarios esperando.
        """

        # 1. Buscar el préstamo activo asociado a este recurso
        prestamo_encontrado = None
        for prestamo in self._prestamos_activos:
            if prestamo.recurso.id == recurso.id:
                prestamo_encontrado = prestamo
                break

        if not prestamo_encontrado:
            print(f"No se encontró ningún préstamo activo para: '{recurso.titulo}'.")
            return False

        # 2. Intentar devolver el recurso (State)
        # Si cambia a Disponible, el propio recurso notificará a sus Observers automáticamente
        if recurso.intentar_devolver():
            prestamo_encontrado.finalizar_prestamo()
            self._prestamos_activos.remove(prestamo_encontrado)
            self._historial_prestamos.append(prestamo_encontrado)
            print(f"Registro de préstamos ID {prestamo_encontrado.id} movido al historial.")
            return True

        return False

    def consultar_prestamos_activos(self):
        """
        Muestra en consola todos los préstamos vigentes.
        """
        print("\n-----------------------------------")
        print("     Listado de préstamos activos    ")
        print("-----------------------------------")
        if not self._prestamos_activos:
            print("No hay préstamos activos en el sistema.")
            return

        for prestamo in self._prestamos_activos:
            fecha_str = prestamo.fecha_prestamo.strftime("%d/%m/%Y %H:%M:%S")
            print(f"ID Préstamo: {prestamo.id}")
            print(f" - Recurso: {prestamo.recurso.obtener_detalles()}")
            print(f" - Solicitante: {prestamo.usuario.apellido}, {prestamo.usuario.nombre} (DNI: {prestamo.usuario.dni})")
            print(f" - Fecha de salida: {fecha_str}")
