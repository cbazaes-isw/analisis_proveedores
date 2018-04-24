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

actecos = list(map(lambda x: ActecoPce(x), lista_Actecos))
resultado = "|".join(map(lambda x: x.Codigo, sorted(actecos)))
