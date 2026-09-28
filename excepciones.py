class ErrorGestionCliente(Exception):
    pass

class RutInvalidoError(ErrorGestionCliente):
    pass

class TelefonoInvalidoError(ErrorGestionCliente):
    pass

class EmailInvalidoError(ErrorGestionCliente):
    pass