def logistic_growth(Pt_1, r, K, years, current_year=1):
    if current_year > years:
        return
    Pt = Pt_1 + r * Pt_1 * (1 - Pt_1 / K)
    print(f"Año {current_year}: Población = {round(Pt)}")
    logistic_growth(Pt, r, K, years, current_year + 1)

# Parámetros iniciales
P0 = 10   # Población inicial
r = 0.2   # Tasa de crecimiento
K = 100   # Capacidad de carga
years = 10  # Número de años a simular

# Ejecutar simulación
print(f"Año 0: Población = {P0}")
logistic_growth(P0, r, K, years)
