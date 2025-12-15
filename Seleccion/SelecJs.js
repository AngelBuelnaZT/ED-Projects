function selectionSort(arr, n) {
    for (let i = 0; i < n - 1; i++) {
        let minIndex = i; // Índice del mínimo actual

        // Buscar el mínimo en el resto del arreglo
        for (let j = i + 1; j < n; j++) {
            if (arr[j] < arr[minIndex]) {
                minIndex = j;
            }
        }

        // Intercambiar el mínimo con el elemento en i
        if (minIndex !== i) {
            let temp = arr[i];
            arr[i] = arr[minIndex];
            arr[minIndex] = temp;
        }
    }
}

function printArray(arr, n) {
    console.log(arr.slice(0, n).join(' '));
}

let arr = [64, 34, 25, 12, 22, 11, 90];
let n = arr.length;

console.log('Arreglo original:');
printArray(arr, n);

selectionSort(arr, n);

console.log('Arreglo ordenado:');
printArray(arr, n);