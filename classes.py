

class cliente(object):
    def __init__(self, rut, idCliente, db):
        self.rut = rut
        self.idCliente = idCliente
        self.db = db

class proveedor(object):
    def __init__(self, rut, cantidad):
        self.rut = rut
        self.cantidad = cantidad

class proveedorPce:
    def __init__(self, dict):
        vars(self).update(dict)
