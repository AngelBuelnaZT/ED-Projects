// Definir una matriz 3x3
const grid = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
];

console.log("Matriz original (3x3):");
// Mostrar la matriz completa
for (const row of grid) {
    console.log(row.join(" "));
}

console.log("\nRecorrido por filas:");
// Mostrar cada fila con sus elementos
grid.forEach((row, i) => {
    console.log(`Fila ${i + 1}: ${row.join(" ")}`);
});

console.log("\nElementos individuales por fila:");
// Mostrar cada elemento con su posición
grid.forEach((row, i) => {
    row.forEach((value, j) => {
        console.log(`Posición [${i},${j}] = ${value}`);
    });
});