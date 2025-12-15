def selection_sort(arr, n):
    for i in range(n - 1):
        min_index = i  # Índice del mínimo actual

        # Buscar el mínimo en el resto del arreglo
        for j in range(i + 1, n):
            if arr[j] < arr[min_index]:
                min_index = j

        # Intercambiar el mínimo con el elemento en i
        if min_index != i:
            arr[i], arr[min_index] = arr[min_index], arr[i]

def print_array(arr, n):
    print(' '.join(map(str, arr[:n])))

arr = [64, 34, 25, 12, 22, 11, 90]
n = len(arr)

print('Arreglo original:')
print_array(arr, n)

selection_sort(arr, n)

print('Arreglo ordenado:')
print_array(arr, n)