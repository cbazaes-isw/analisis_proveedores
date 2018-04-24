from classes import ActecoPce

lista_Actecos =[
    {
        "Codigo": "345",
        "Nombre": "sample string 2",
        "AffectoIva": "sample string 3"
    },
    {
        "Codigo": "759",
        "Nombre": "sample string 2",
        "AffectoIva": "sample string 3"
    },
    {
        "Codigo": "138",
        "Nombre": "sample string 2",
        "AffectoIva": "sample string 3"
    },
    {
        "Codigo": "486",
        "Nombre": "sample string 2",
        "AffectoIva": "sample string 3"
    },
    {
        "Codigo": "645",
        "Nombre": "sample string 2",
        "AffectoIva": "sample string 3"
    },
    {
        "Codigo": "598",
        "Nombre": "sample string 2",
        "AffectoIva": "sample string 3"
    }
]


from functools import reduce

actecos = list(map(lambda x: ActecoPce(x), lista_Actecos))
actecos_ordenados = sorted(actecos)
resultado = reduce(lambda x,y: "{}|{}".format(x.Codigo,y.Codigo), actecos_ordenados)
