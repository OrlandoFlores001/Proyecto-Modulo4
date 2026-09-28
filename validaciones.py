from excepciones import RutInvalidoError, TelefonoInvalidoError, EmailInvalidoError

class Validador:
    @staticmethod
    def validar_rut(rut: str) -> str:
        rut_limpio = rut.replace(".", "").replace("-", "").strip().upper()
        if len(rut_limpio) < 8 or len(rut_limpio) > 9:
            raise RutInvalidoError("El RUT/DNI debe contener entre 8 y 9 caracteres válidos.")
        return rut_limpio

    @staticmethod
    def validar_telefono(telefono: str) -> str:
        tel_limpio = telefono.strip().replace("+", "")
        if not tel_limpio.isdigit() or len(tel_limpio) < 8:
            raise TelefonoInvalidoError("El teléfono debe contener únicamente números (mínimo 8 dígitos).")
        return telefono.strip()

    @staticmethod
    def validar_email(email: str) -> str:
        correo_limpio = email.strip()
        if "@" not in correo_limpio or "." not in correo_limpio:
            raise EmailInvalidoError("El correo electrónico debe contener un '@' y un dominio válido.")
        return correo_limpio