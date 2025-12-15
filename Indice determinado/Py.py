
numeros = [10, 20, 30, 40, 50]

valor_a_insertar = 25

indice = 2

# Verificar si el índice es válido
if 0 <= indice <= len(numeros):
    numeros.insert(indice, valor_a_insertar)
else:
    print("Índice fuera de rango.")

# Mostrar el contenido actualizado de la lista
print("Lista actualizada:", numeros)
