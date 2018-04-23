# pylint: disable=C0103
"""
Análisis de proveedores
"""

import csv
import json
from datetime import datetime

import requests

import pyodbc
from classes import proveedor, proveedorBd, proveedorPce


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
            pPce = json.loads(response_pce.text, object_hook=proveedorPce)
            procesaProveedor(pDict[p], pPce)
        else:
            print(response_pce.text)

def procesaProveedor(pBd, pPce):
    """
    procesaProveedores method
    """
    formato = ("{p.rutProveedor},{p.cantidad},{p.Tramo_Ventas},{p.Numero_Trabajadores},{p.Rubro}," +
               "{p.Subrubro},{p.Actividad_Economica},{p.Region},{p.Comuna},{p.Calle},{p.Numero},{p.Bloque}," +
               "{p.Villa_Poblacion},{p.Fecha_Inicio},{p.Fecha_Termino_Giro},{p.Tipo_Termino_Giro}," +
               "{p.Tipo_Contribuyente},{p.SubTipoContribuyente},{p.F22_C_645},{p.F22_C_646}," +
               "{p.FechaResolucion},{p.NumResolucion},{p.MailIntercambio}")
    row = formato.format(p=pBd)
    i = 1

main()
