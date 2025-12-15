# Crear la lista
arreglo = [12, 45, 23, 67, 89, 34]
valor_buscado = 67
encontrado = False

# Búsqueda del valor
for i in range(len(arreglo)):
    if arreglo[i] == valor_buscado:
        print(f"Valor encontrado en el índice {i}")
        encontrado = True
        break

# Si no se encontró
if not encontrado:
    print("Valor no encontrado en el arreglo.")
