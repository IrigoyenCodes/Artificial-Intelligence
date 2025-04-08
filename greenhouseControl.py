Greenhouse = {
    "Llueve": True,
    "No llueve": False,
    "Hay nieve": False,
    "Mayor a 25C": True,
    "Menor a 10C": False
}

def efecto_invernadero(proposiciones):
    """Determina el impacto del clima en la humedad y ventilación."""
    
    if proposiciones["Llueve"] and proposiciones["Mayor a 25C"]:
        return "Hay humedad y necesitamos ventilación"
    elif proposiciones["Llueve"]:
        return "Hay lluvia, verificar drenaje"
    elif proposiciones["Mayor a 25C"]:
        return "Hace calor, se recomienda ventilación"
    elif proposiciones["Menor a 10C"]:
        return "Hace frio, se recomienda un calentador"
    elif proposiciones["Hay nieve"]:
        return "Esta nevando, se recomienda un calentador"
    else:
        return "Condiciones normales"

# Llamada a la función
print(efecto_invernadero(Greenhouse))

Greenhouse_nuevo1 = {
    "Llueve": False,
    "No llueve": False,
    "Hay nieve": False,
    "Mayor a 25C": True,
    "Menor a 10C": False
}

print(efecto_invernadero(Greenhouse_nuevo1))

Greenhouse_nuevo2 = {
    "Llueve": False,
    "No llueve": False,
    "Hay nieve": False,
    "Mayor a 25C": False,
    "Menor a 10C": True
}

print(efecto_invernadero(Greenhouse_nuevo2))
