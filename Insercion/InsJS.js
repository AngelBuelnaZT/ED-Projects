function insertionSort(arr, n) {
    for (let i = 1; i < n; i++) {
        let key = arr[i]; // Elemento a insertar
        let j = i - 1;    // Índice del último elemento de la porción ordenada

        // Desplazar elementos mayores hacia la derecha
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j--;
        }
        arr[j + 1] = key; // Insertar el elemento en la posición correcta
    }
}

function printArray(arr, n) {
    for (let i = 0; i < n; i++) {
        process.stdout.write(arr[i] + " ");
    }
    console.log();
}

let arr = [64, 34, 25, 12, 22, 11, 90];
let n = arr.length;

console.log("Arreglo original: ");
printArray(arr, n);

insertionSort(arr, n);

console.log("Arreglo ordenado: ");
printArray(arr, n);