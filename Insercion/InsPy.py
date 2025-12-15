def insertion_sort(arr, n):
    for i in range(1, n):
        key = arr[i]  # Elemento a insertar
        j = i - 1     # Índice del último elemento de la porción ordenada

        # Desplazar elementos mayores hacia la derecha
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key  # Insertar el elemento en la posición correcta

def print_array(arr, n):
    for i in range(n):
        print(arr[i], end=" ")
    print()

arr = [64, 34, 25, 12, 22, 11, 90]
n = len(arr)

print("Arreglo original: ")
print_array(arr, n)

insertion_sort(arr, n)

print("Arreglo ordenado: ")
print_array(arr, n)