# pylint: disable=C0103
"""
Análisis de proveedores
"""
import csv
import json
import os
import queue
import sys
import threading
import time
from datetime import datetime

import requests

import pyodbc
from classes import proveedorBd, proveedorPce


def main():
    """
    main method
    """
    queue_rut_contribuyentes = queue.Queue(maxsize=0)
    num_threads = config["threads"]["num_threads"]
    
    # Conexión a la base de datos
    cnn = pyodbc.connect(config["db"]["connection_string"], autocommit=True)

    for i in range(num_threads):
        t = threading.Thread(target=worker, args=(queue_rut_contribuyentes, cnn))
        t.setDaemon(True)
        t.start()

    getRutContribuyentes(queue_rut_contribuyentes, cnn)

    queue_rut_contribuyentes.join()

    cnn.close()

def worker(q, cnn):
    while True:
        rut = q.get()
        procesaRUT(rut, cnn)
        time.sleep(config["threads"]["sec_sleep"])
        q.task_done()

def procesaRUT(rut, cnn):
    # Ejecutando una petición a la API de PCE para
    # obtener más información acerca del contribuyente
    try:
        response_pce = requests.post(
            config["api"]["pce"]["endpoint"].format(rut_empresa=rut),
            data=json.dumps(config["api"]["pce"]["request_body"]),
            headers=config["api"]["pce"]["request_header"])

        if response_pce.ok:
            print("\n{} Proveedor {rut:>11}... Ok!".format(str(datetime.now()), rut=rut), end="")
            pPce = proveedorPce(response_pce.json())
            pPce.Mensaje = "OK"
        else:
            print("\n{} Proveedor {rut:>11}: {} ".format(str(datetime.now()), response_pce.text, rut=rut), end="")
            pPce = proveedorPce({})
            pPce.Mensaje = response_pce.text
        
        cursor = cnn.cursor()
        cursor.execute(config["db"]["update_format"], pPce.RazonSocial, pPce.Giro, pPce.Direccion,
            pPce.DireccionRegional, pPce.NumeroResolucion, pPce.FechaResolucion, pPce.CodigosActecos,
            pPce.CodigosDocumentosProduccion, pPce.Mensaje, rut)
        cnn.commit()
    except (pyodbc.DataError, pyodbc.Error) as e:
        print("\n{} Proveedor {rut:>11}... ERROR: {clase} - {error}".format(str(datetime.now()), clase=sys.exc_info()[0], error=e, rut=rut), end="")
    except:
        print("\n{} Proveedor {rut:>11}... ERROR: {clase}".format(str(datetime.now()), clase=sys.exc_info()[0], rut=rut), end="")

def getConfiguracion():
    config_file = open("configuracion.json")
    config = json.load(config_file)
    config_file.close()
    return config

def getRutContribuyentes(q, cnn):
    # Conexión a la base de datos y ejecución de la consulta
    print("\n{} Ejecutando la consulta...".format(str(datetime.now())), end="")
    
    query_file = open(config["db"]["query_file"])
    cmd = query_file.read()
    query_file.close()
    cursor = cnn.cursor()
    cursor.execute(cmd)
    
    # Procesando los registros
    print("\n{} Recuperando resultados...".format(str(datetime.now())), end="")
    rows = cursor.fetchall()
    for row in rows:
        q.put(row.rut)

# Configuracion
config = getConfiguracion()

main()
