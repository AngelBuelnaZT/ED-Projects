# Definir una matriz de 3x3
tabla = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

print("Visualización de la matriz original:")
# Imprimir la matriz inicial
for renglon in range(3):
    linea = ""
    for posicion in range(3):
        linea += str(tabla[renglon][posicion]) + "  "
    print(linea)

print("\nExploración por columnas:")
# Recorrer la matriz por columnas
for col in range(3):
    datos_columna = f"Columna {col + 1}: "
    for reng in range(3):
        datos_columna += str(tabla[reng][col]) + "  "
    print(datos_columna)
