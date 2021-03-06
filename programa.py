# pylint: disable=C0103
"""
Análisis de proveedores
"""

import csv
import json
import os
import queue
import threading
from datetime import datetime

import requests

import pyodbc
from classes import proveedorBd, proveedorPce


def main():
    """
    main method
    """
    queue_proveedores = queue.Queue(maxsize=0)
    num_threads = config["threads"]["num_threads"]

    # Abro/creo el archivo y escribo el encabezado de las columnas
    archivo = open(config["output"]["filename"],"a")
    archivo.write(config["output"]["row_format"])

    for i in range(num_threads):
        t = threading.Thread(target=worker, args=(queue_proveedores, archivo))
        t.setDaemon(True)
        t.start()

    getProveedoresBd(queue_proveedores, archivo)

    queue_proveedores.join()
    archivo.close()

def worker(q, archivo):
    while True:
        pBd = q.get()
        procesaProveedor(pBd, archivo)
        q.task_done()

def procesaProveedor(p, archivo):
    # Ejecutando una petición a la API de PCE para
    # obtener más información acerca del contribuyente
    response_pce = requests.post(
        config["api"]["pce"]["endpoint"].format(rut_empresa=p.rutProveedor),
        data=json.dumps(config["api"]["pce"]["request_body"]),
        headers=config["api"]["pce"]["request_header"])

    if not response_pce.ok:
        print("\n{} Proveedor {rut:>11}: {} ".format(str(datetime.now()), response_pce.text, rut=p.rutProveedor), end="")
        return
    
    print("\n{} Proveedor {rut:>11}... Ok!".format(str(datetime.now()), rut=p.rutProveedor), end="")

    pPce = proveedorPce(response_pce.json())
    # Obtengo el registro del archivo que corresonde al 
    # proveedor que estoy procesando en este momento
    formato = config["output"]["row_format"]
    
    row = formato.format(bd=p, pce=pPce)
    archivo.write(row)

def getConfiguracion():
    config_file = open("configuracion.json")
    config = json.load(config_file)
    config_file.close()
    return config

def getProveedoresBd(q, f):
    # Conexión a la base de datos y ejecución de la consulta
    print("\n{} Ejecutando la consulta...".format(str(datetime.now())), end="")
    cnn = pyodbc.connect(config["db"]["connection_string"])
    query_file = open(config["db"]["query_file"])
    cmd = query_file.read()
    query_file.close()
    cursor = cnn.cursor()
    cursor.execute(cmd)
    
    # Procesando los registros
    print("\n{} Recuperando resultados...".format(str(datetime.now())), end="")
    results = cursor.fetchone()
    while results:
        q.put(proveedorBd(results))
        results = cursor.fetchone()

    cnn.close()

# Configuracion
config = getConfiguracion()

main()
