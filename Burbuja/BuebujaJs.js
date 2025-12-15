function bubbleSort(arr, n) {
    let swapCounter = 0;
    let swapped;

    do {
        swapped = false;
        for (let i = 1; i < n; ++i) {
            if (arr[i - 1] > arr[i]) {
                let temp = arr[i - 1];
                arr[i - 1] = arr[i];
                arr[i] = temp;
                swapped = true;
                ++swapCounter;
            }
        }
        --n;
    } while (swapped);

    return swapCounter;
}

const SIZE = 15;
let arr = new Array(SIZE);

console.log("Array original (valores aleatorios):");
for (let i = 0; i < SIZE; ++i) {
    arr[i] = Math.floor(Math.random() * 100) + 1; // 1 to 100
    process.stdout.write(arr[i] + " ");
}
console.log();

let swapCounter = bubbleSort(arr, SIZE);

console.log("\nArray ordenado:");
for (let i = 0; i < SIZE; ++i) {
    process.stdout.write(arr[i] + " ");
}

console.log("\n\nTotal de intercambios realizados: " + swapCounter);