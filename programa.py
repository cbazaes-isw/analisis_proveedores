# pylint: disable=C0103
"""
Análisis de proveedores
"""

import csv
import json
from datetime import datetime

import requests

import pyodbc
from classes import proveedorBd, proveedorPce


def main():
    """
    main method
    """
    # Configuracion
    config_file = open("configuracion.json")
    config = json.load(config_file)
    config_file.close()

    # Conexión a la base de datos y ejecución de la consulta
    print("{} Ejecutando la consulta...".format(str(datetime.now())))
    cnn = pyodbc.connect(config["db"]["connection_string"])
    query_file = open(config["db"]["query_file"])
    cmd = query_file.read()
    query_file.close()
    cursor = cnn.cursor()
    cursor.execute(cmd)

    # Procesando los registros
    print("{} Obteniendo los proveedores...".format(str(datetime.now())))
    pDict = {}
    results = cursor.fetchone()
    while results:
        pDict[results.rutProveedor] = proveedorBd(results)
        results = cursor.fetchone()

    cnn.close()

    # Revisando la información
    print("{} Procesando {} proveedores...".format(str(datetime.now()), len(pDict)))
    #for c in clientes:
    for p in pDict:
        response_pce = requests.post(
            config["api"]["pce"]["endpoint"].format(rut_empresa=p),
            data=json.dumps(config["api"]["pce"]["request_body"]),
            headers=config["api"]["pce"]["request_header"])
        if response_pce.ok:
            pPce = proveedorPce(response_pce.json())
            procesaProveedor(pDict[p], pPce)
        else:
            print(response_pce.text)

def procesaProveedor(pBd, pPce):
    """
    procesaProveedores method
    """
    formato = ("{bd.rutProveedor},{bd.cantidad},{bd.Tramo_Ventas},{bd.Numero_Trabajadores},{bd.Rubro}," +
               "{bd.Subrubro},{bd.Actividad_Economica},{bd.Region},{bd.Comuna},{bd.Calle},{bd.Numero},{bd.Bloque}," +
               "{bd.Villa_Poblacion},{bd.Fecha_Inicio},{bd.Fecha_Termino_Giro},{bd.Tipo_Termino_Giro}," +
               "{bd.Tipo_Contribuyente},{bd.SubTipoContribuyente},{bd.F22_C_645},{bd.F22_C_646}," +
               "{bd.FechaResolucion},{bd.NumResolucion},{bd.MailIntercambio},"
               "{pce.getCodigosActecos},{pce.getCodigosDocumentosProduccion}")
    row = formato.format(bd=pBd, pce=pPce)
    i = 1

main()
