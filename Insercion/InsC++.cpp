#include <iostream>
using namespace std;

void insertionSort(int arr[], int n) {
    for (int i = 1; i < n; i++) {
        int key = arr[i]; // Elemento a insertar
        int j = i - 1;    // Índice del último elemento de la porción ordenada

        // Desplazar elementos mayores hacia la derecha
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j--;
        }
        arr[j + 1] = key; // Insertar el elemento en la posición correcta
    }
}

// Función para imprimir el arreglo
void printArray(int arr[], int n) {
    for (int i = 0; i < n; i++) {
        cout << arr[i] << " ";
    }
    cout << endl;
}

int main() {
    int arr[] = {64, 34, 25, 12, 22, 11, 90};
    int n = sizeof(arr) / sizeof(arr[0]);

    cout << "Arreglo original: ";
    printArray(arr, n);

    insertionSort(arr, n);

    cout << "Arreglo ordenado: ";
    printArray(arr, n);

    return 0;
}