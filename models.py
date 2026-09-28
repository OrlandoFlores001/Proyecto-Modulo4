from validaciones import Validador

class Cliente:
    def __init__(self, rut: str, nombre: str, correo: str, telefono: str, password: str, rol: str = "Regular"):
        self.__rut = Validador.validar_rut(rut)
        self.__nombre = nombre.strip()
        self.__correo = Validador.validar_email(correo)
        self.__telefono = Validador.validar_telefono(telefono)
        self.__password = password.strip()
        self.__rol = rol

    @property
    def rut(self):
        return self.__rut

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self.__nombre = valor.strip()

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        self.__correo = Validador.validar_email(valor)

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        self.__telefono = Validador.validar_telefono(valor)

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, valor):
        self.__password = valor.strip()

    @property
    def rol(self):
        return self.__rol

    @rol.setter
    def rol(self, nuevo_rol):
        self.__rol = nuevo_rol

    def puede_eliminar(self) -> bool:
        return False

    def puede_vaciar(self) -> bool:
        return False

    def puede_modificar_roles(self) -> bool:
        return False

    def __str__(self):
        return f"[{self.__rol}] RUT: {self.__rut} | Nombre: {self.__nombre} | Email: {self.__correo} | Tel: {self.__telefono}"

    def __eq__(self, otro):
        if isinstance(otro, Cliente):
            return self.__rut == otro.rut
        return False

    def to_dict(self):
        return {
            "rut": self.__rut,
            "nombre": self.__nombre,
            "correo": self.__correo,
            "telefono": self.__telefono,
            "password": self.__password,
            "rol": self.__rol
        }

class ClienteRegular(Cliente):
    def __init__(self, rut, nombre, correo, telefono, password):
        super().__init__(rut, nombre, correo, telefono, password, "Regular")


class ClientePremium(Cliente):
    def __init__(self, rut, nombre, correo, telefono, password):
        super().__init__(rut, nombre, correo, telefono, password, "Premium")

    def puede_eliminar(self):
        return True


class ClienteCorporativo(Cliente):
    def __init__(self, rut, nombre, correo, telefono, password):
        super().__init__(rut, nombre, correo, telefono, password, "Corporativo")

    def puede_eliminar(self):
        return True

    def puede_modificar_roles(self):
        return True


class AdminMain(Cliente):
    def __init__(self, rut, nombre, correo, telefono, password):
        super().__init__(rut, nombre, correo, telefono, password, "AdminMain")

    def puede_eliminar(self):
        return True

    def puede_vaciar(self):
        return True

    def puede_modificar_roles(self):
        return True