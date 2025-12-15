import random

def bubble_sort(arr, n):
    swap_counter = 0
    swapped = True

    while swapped:
        swapped = False
        for i in range(1, n):
            if arr[i - 1] > arr[i]:
                arr[i - 1], arr[i] = arr[i], arr[i - 1] # Python swap
                swapped = True
                swap_counter += 1
        n -= 1

    return swap_counter

SIZE = 15
arr = []

print("Array original (valores aleatorios):")
for i in range(SIZE):
    arr.append(random.randint(1, 100)) # 1 to 100
    print(arr[i], end=" ")
print()

swap_counter = bubble_sort(arr, SIZE)

print("\nArray ordenado:")
for i in range(SIZE):
    print(arr[i], end=" ")

print("\n\nTotal de intercambios realizados:", swap_counter)