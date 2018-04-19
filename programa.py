import json
import pyodbc
import urllib.parse
import requests
from classes import proveedor
from classes import proveedorPce
from datetime import datetime


def main():
    # Configuracion
    config_file = open("configuracion.json", "r")
    config = json.load(config_file)

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
            rut = results[0],
            cantidad = results[1]
        ))

        results = cursor.fetchone()

    cnn.close()

    # Revisando la información
    print("{} Procesando los proveedores...".format(str(datetime.now())))
    #for c in clientes:
    for p in proveedores:
        response_pce = requests.post(endpoint_pce.format(rut_empresa=p.rut), data=data_pce, headers=headers_pce)
        if (response_pce.ok):
            provPce = json.loads(response_pce.text, object_hook=proveedorPce)            
            print(json_proveedor_pce)
        else:
            print(response_pce.text)

def procesaProveedor(proveedor):
    pass



main()