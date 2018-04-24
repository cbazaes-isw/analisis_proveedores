from functools import reduce
from operator import attrgetter


class ActecoPce:
    def __init__(self, dict):
        self.Codigo = dict["Codigo"]
        self.Nombre = dict["Nombre"]
        self.AffectoIva = dict["AffectoIva"]

    def __repr__(self):
        return "{}: {} {}".format(self.__class__.__name__, self.Codigo, self.Nombre)
    
    def __lt__(self, other):
        return self.Codigo < other.Codigo

class TipoDocumentoPce:
    def __init__(self, dict):
        self.Codigo = dict["Codigo"]
        self.Nombre = dict["Nombre"]
        self.FechaPermitido = dict["FechaPermitido"]
        self.FechaDenegado = dict["FechaDenegado"]

    def __repr__(self):
        return "{}: {} {}".format(self.__class__.__name__, self.Codigo, self.Nombre)

    def __lt__(self, other):
        return self.Codigo < other.Codigo

class proveedorPce:
    def __init__(self, dict):
        self.RUT = dict["RUT"]
        self.RazonSocial = dict["RazonSocial"]
        self.Giro = dict["Giro"]
        self.Direccion = dict["Direccion"]
        self.DireccionRegional = dict["DireccionRegional"]
        self.NumeroResolucion = dict["NumeroResolucion"]
        self.FechaResolucion = dict["FechaResolucion"]
        self.Actecos = list(map(lambda x: ActecoPce(x), dict["Actecos"]))
        self.DocumentosHomo = list(map(lambda x: TipoDocumentoPce(x), dict["DocumentosHomo"]))
        self.DocumentosProd = list(map(lambda x: TipoDocumentoPce(x), dict["DocumentosProd"]))

    def __repr__(self):
        return "{}: {} {}".format(self.__class__.__name__, self.RUT, self.RazonSocial)

    def getCodigosActecos(self):
        resultado = "|".join(map(lambda x: x.Codigo, sorted(self.Actecos)))
        return resultado

    def getCodigosDocumentosProduccion(self):
        resultado = "|".join(map(lambda x: x.Codigo, sorted(self.DocumentosProd)))
        return resultado

    def getCodigosDocumentosCertificacion(self):
        resultado = "|".join(map(lambda x: x.Codigo, sorted(self.DocumentosHomo)))
        return resultado

class proveedorBd:
    def __init__(self, provBd):
        self.rutProveedor = provBd.rutProveedor
        self.cantidad = provBd.cantidad
        self.Tramo_Ventas = provBd.Tramo_Ventas
        self.Numero_Trabajadores = provBd.Numero_Trabajadores
        self.Rubro = provBd.Rubro.replace(",","")
        self.Subrubro = provBd.Subrubro.replace(",","")
        self.Actividad_Economica = provBd.Actividad_Economica.replace(",","")
        self.Region = provBd.Region.replace(",","")
        self.Comuna = provBd.Comuna.replace(",","")
        self.Calle = provBd.Calle.replace(",","")
        self.Numero = provBd.Numero.replace(",","")
        self.Bloque = provBd.Bloque.replace(",","")
        self.Villa_Poblacion = provBd.Villa_Poblacion.replace(",","")
        self.Fecha_Inicio = provBd.Fecha_Inicio
        self.Fecha_Termino_Giro = provBd.Fecha_Termino_Giro
        self.Tipo_Termino_Giro = provBd.Tipo_Termino_Giro.replace(",","")
        self.Tipo_Contribuyente = provBd.Tipo_Contribuyente.replace(",","")
        self.SubTipoContribuyente = provBd.SubTipoContribuyente.replace(",","")
        self.F22_C_645 = provBd.F22_C_645
        self.F22_C_646 = provBd.F22_C_646
        self.FechaResolucion = provBd.FechaResolucion
        self.NumResolucion = provBd.NumResolucion
        self.MailIntercambio = provBd.MailIntercambio

    def __repr__(self):
        return "{}: {}".format(self.__class__.__name__, self.rutProveedor)
