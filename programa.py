# pylint: disable=C0103
"""
DOCSTRING
"""

import json
from datetime import datetime
import pyodbc
import requests
import csv
from classes import proveedor
from classes import proveedorPce


def main():
    """
    DOCSTRING
    """
    # Configuracion
    config_file = open("configuracion.json", "r")
    config = json.load(config_file)
    config_file.close()

    connection_string = config["db"]["connection_string"]
    path_query_file = config["db"]["query_file"]

    endpoint_pce = config["api"]["pce"]["endpoint"]
    headers_pce = config["api"]["pce"]["request_header"]
    data_pce = json.dumps(config["api"]["pce"]["request_body"])

    # Conexión a la base de datos y ejecución de la consulta
    print("{} Ejecutando la consulta...".format(str(datetime.now())))
    cnn = pyodbc.connect(connection_string)
    query_file = open(path_query_file, "r")
    cmd = query_file.read()
    query_file.close()
    cursor = cnn.cursor()
    cursor.execute(cmd)

    # Procesando los registros
    print("{} Obteniendo los proveedores...".format(str(datetime.now())))
    proveedores = [] # [0] db, [1] Contenedor, [2] RutProveedor, [3] Cantidad
    results = cursor.fetchone()
    while results:
        proveedores.append(proveedor(
            rut=results[0],
            cantidad=results[1]
        ))

        results = cursor.fetchone()

    cnn.close()

    # Revisando la información
    print("{} Procesando los proveedores...".format(str(datetime.now())))
    #for c in clientes:
    for pBd in proveedores:
        response_pce = requests.post(
            endpoint_pce.format(rut_empresa=pBd.rut),
            data=data_pce,
            headers=headers_pce)
        if response_pce.ok:
            pPce = json.loads(response_pce.text, object_hook=proveedorPce)
            procesaProveedor(pPce, pBd)
        else:
            print(response_pce.text)

def procesaProveedor(pBd, pPce):
    """
    DOCSTRING
    """
    formato = ("{rutProveedor},{cantidad},{Tramo_Ventas},{Numero_Trabajadores},{Rubro}," +
               "{Subrubro},{Actividad_Economica},{Region},{Comuna},{Calle},{Numero},{Bloque}," +
               "{Villa_Poblacion},{Fecha_Inicio},{Fecha_Termino_Giro},{Tipo_Termino_Giro}," +
               "{Tipo_Contribuyente},{SubTipoContribuyente},{F22_C_645},{F22_C_646}," +
               "{FechaResolucion},{NumResolucion},{MailIntercambio}")




main()
