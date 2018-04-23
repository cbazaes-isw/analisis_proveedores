
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

class proveedorBd:
    def __init__(self, provDict):
        self.rutProveedor = provDict.rutProveedor
        self.cantidad = provDict.cantidad
        self.Tramo_Ventas = provDict.Tramo_Ventas
        self.Numero_Trabajadores = provDict.Numero_Trabajadores
        self.Rubro = provDict.Rubro.replace(",","")
        self.Subrubro = provDict.Subrubro.replace(",","")
        self.Actividad_Economica = provDict.Actividad_Economica.replace(",","")
        self.Region = provDict.Region.replace(",","")
        self.Comuna = provDict.Comuna.replace(",","")
        self.Calle = provDict.Calle.replace(",","")
        self.Numero = provDict.Numero.replace(",","")
        self.Bloque = provDict.Bloque.replace(",","")
        self.Villa_Poblacion = provDict.Villa_Poblacion.replace(",","")
        self.Fecha_Inicio = provDict.Fecha_Inicio
        self.Fecha_Termino_Giro = provDict.Fecha_Termino_Giro
        self.Tipo_Termino_Giro = provDict.Tipo_Termino_Giro.replace(",","")
        self.Tipo_Contribuyente = provDict.Tipo_Contribuyente.replace(",","")
        self.SubTipoContribuyente = provDict.SubTipoContribuyente.replace(",","")
        self.F22_C_645 = provDict.F22_C_645
        self.F22_C_646 = provDict.F22_C_646
        self.FechaResolucion = provDict.FechaResolucion
        self.NumResolucion = provDict.NumResolucion
        self.MailIntercambio = provDict.MailIntercambio
