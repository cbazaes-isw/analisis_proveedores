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

    print("{} Ejecutando la consulta...".format(str(datetime.now())))
    pDict = getProvedoresBd()

    # Revisando la información
    print("{} Procesando {} proveedores...".format(str(datetime.now()), len(pDict)))
    archivo = open(config["output_file"],"a")
    try:
        for rut in pDict:
            print("{} procesando {rut:>10}... ".format(str(datetime.now()), rut=rut),end='', flush=True)
            # Ejecutando una petición a la API de PCE para
            # obtener más información acerca del contribuyente
            response_pce = requests.post(
                config["api"]["pce"]["endpoint"].format(rut_empresa=rut),
                data=json.dumps(config["api"]["pce"]["request_body"]),
                headers=config["api"]["pce"]["request_header"])

            if not response_pce.ok:
                print(response_pce.text)
                continue

            print("OK!")
            pPce = proveedorPce(response_pce.json())
            # Obtengo el registro del archivo que corresonde al 
            # proveedor que estoy procesando en este momento
            row = procesaProveedor(pDict[rut], pPce)
            archivo.write(row)

    except:
        archivo.close()
    finally:
        archivo.close()

def procesaProveedor(pBd, pPce):
    """
    procesaProveedores method
    """
    formato = ("{bd.rutProveedor};{bd.cantidad};{bd.Tramo_Ventas};{bd.Numero_Trabajadores};" +
               "{bd.Rubro};{bd.Subrubro};{bd.Actividad_Economica};{bd.Region};{bd.Comuna};" +
               "{bd.Calle};{bd.Numero};{bd.Bloque};{bd.Villa_Poblacion};{bd.Fecha_Inicio};" +
               "{bd.Fecha_Termino_Giro};{bd.Tipo_Termino_Giro};{bd.Tipo_Contribuyente};" +
               "{bd.SubTipoContribuyente};{bd.F22_C_645};{bd.F22_C_646};{bd.FechaResolucion};" +
               "{bd.NumResolucion};{bd.MailIntercambio};{pce.CodigosActecos};" +
               "{pce.CodigosDocumentosProduccion}\n")
    row = formato.format(bd=pBd, pce=pPce)
    return row

def getConfiguracion():
    config_file = open("configuracion.json")
    config = json.load(config_file)
    config_file.close()
    return config

def getProvedoresBd():
    # Conexión a la base de datos y ejecución de la consulta
    cnn = pyodbc.connect(config["db"]["connection_string"])
    query_file = open(config["db"]["query_file"])
    cmd = query_file.read()
    query_file.close()
    cursor = cnn.cursor()
    cursor.execute(cmd)
    
    # Procesando los registros
    pDict = {}
    results = cursor.fetchone()
    while results:
        pDict[results.rutProveedor] = proveedorBd(results)
        results = cursor.fetchone()

    cnn.close()

    return pDict

# Configuracion
config = getConfiguracion()

main()
