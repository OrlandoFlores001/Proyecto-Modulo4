# basededatos.py
import os
from models import ClienteRegular, ClientePremium, ClienteCorporativo, AdminMain, Cliente

ARCHIVO_BD = "clientes.txt"

class GestorPersistencia:
    @staticmethod
    def cargar_clientes():
        """Lee el archivo clientes.txt y convierte cada línea en un objeto Cliente."""
        if not os.path.exists(ARCHIVO_BD):
            return []

        clientes = []
        try:
            with open(ARCHIVO_BD, "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    partes = linea.strip().split(" | ")
                    if len(partes) >= 6:
                        rut, nombre, correo, telefono, password, rol = partes[:6]
                        
                        if rol == "Premium":
                            cliente_obj = ClientePremium(rut, nombre, correo, telefono, password)
                        elif rol == "Corporativo":
                            cliente_obj = ClienteCorporativo(rut, nombre, correo, telefono, password)
                        elif rol == "AdminMain":
                            cliente_obj = AdminMain(rut, nombre, correo, telefono, password)
                        else:
                            cliente_obj = ClienteRegular(rut, nombre, correo, telefono, password)
                            
                        clientes.append(cliente_obj)
            return clientes
        except Exception as e:
            print(f"Error al cargar archivo: {e}")
            return []

    @staticmethod
    def guardar_todos(lista_clientes):
        """Reescribe todo el archivo clientes.txt en formato texto plano con ' | '."""
        with open(ARCHIVO_BD, "w", encoding="utf-8") as archivo:
            for cliente in lista_clientes:
                linea = f"{cliente.rut} | {cliente.nombre} | {cliente.correo} | {cliente.telefono} | {cliente.password} | {cliente.rol}\n"
                archivo.write(linea)

    @staticmethod
    def agregar_cliente(cliente: Cliente):
        """Agrega un cliente validando duplicados con __eq__ y guardando en clientes.txt."""
        clientes = GestorPersistencia.cargar_clientes()
        if cliente in clientes:
            raise ValueError("Ya existe un cliente registrado con ese RUT.")
            
        clientes.append(cliente)
        GestorPersistencia.guardar_todos(clientes)

    @staticmethod
    def eliminar_cliente(rut: str):
        """Elimina un cliente de clientes.txt mediante su RUT."""
        clientes = GestorPersistencia.cargar_clientes()
        clientes_filtrados = [c for c in clientes if c.rut != rut]
        GestorPersistencia.guardar_todos(clientes_filtrados)

    @staticmethod
    def vaciar_bd():
        """Deja el archivo clientes.txt completamente vacío."""
        GestorPersistencia.guardar_todos([])