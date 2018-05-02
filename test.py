import pyodbc

cnn = pyodbc.connect("Driver={SQL Server};Server=52.201.227.21;Database=Pyme;uid=sa;pwd=S0leM0le123*")
cmd = "select idempresa [ID empresa], codlegal [Código legal], nombre [Razón social] from empresa"
cursor = cnn.cursor()
cursor.execute(cmd)

header = ";".join(map(lambda c: c[0], cursor.description)) + "\n"

print(header)

cnn.close()
