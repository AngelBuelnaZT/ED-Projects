# Definir una matriz 3x3
grid = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

print("Matriz original (3x3):")
# Mostrar la matriz completa
for row in grid:
    print(" ".join(str(num) for num in row))

print("\nRecorrido por filas:")
# Mostrar cada fila con sus elementos
for i, row in enumerate(grid, 1):
    print(f"Fila {i}: {' '.join(str(num) for num in row)}")

print("\nElementos individuales por fila:")
# Mostrar cada elemento con su posición
for i, row in enumerate(grid):
    for j, value in enumerate(row):
        print(f"Posición [{i},{j}] = {value}")