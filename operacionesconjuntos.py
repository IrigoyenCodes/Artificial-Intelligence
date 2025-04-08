# Definición de las operaciones sobre los conjuntos

def union(A, B):
    return A | B  # Unión de A y B

def interseccion(A, B):
    return A & B  # Intersección de A y B

def complemento(A):
    universo = {0, 1}
    return universo - A  # Complemento de A con respecto al universo

def diferencia(A, B):
    return A - B  # Diferencia A - B

# Definición de los conjuntos A y B (pueden tomar solo 0 o 1)
A = {1}  # 1 representa "verdadero"
B = {0}  # 0 representa "falso"

# Imprimir los resultados en formato de tabla
print("+-------------------------------|---------------------+")
print("| Operación                     |    Resultado        |")
print("+-------------------------------|---------------------+")
print(f"| Unión (A ∪ B)                 |        {union(A, B)}       |")
print(f"| Intersección (A ∩ B)          |          {interseccion(A, B)}      |")
print(f"| Complemento de A (A')         |          {complemento(A)}        |")
print(f"| Diferencia (A - B)            |          {diferencia(A, B)}        |")
print("+-------------------------------|---------------------+")
