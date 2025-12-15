// Definir una matriz de 3x3
const tabla = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
];

console.log("Visualización de la matriz original:");
// Imprimir la matriz inicial
for (let renglon = 0; renglon < 3; renglon++) {
    let linea = "";
    for (let posicion = 0; posicion < 3; posicion++) {
        linea += tabla[renglon][posicion] + "  ";
    }
    console.log(linea);
}

console.log("\nExploración por columnas:");
// Recorrer la matriz por columnas
for (let col = 0; col < 3; col++) {
    let datosColumna = `Columna ${col + 1}: `;
    for (let reng = 0; reng < 3; reng++) {
        datosColumna += tabla[reng][col] + "  ";
    }
    console.log(datosColumna);
}

console.log("\nDetalles de elementos por columna:");
// Mostrar cada elemento individualmente por columna
for (let col = 0; col < 3; col++) {
    for (let reng = 0; reng < 3; reng++) {
        console.log(`Valor en posición [${reng},${col}] = ${tabla[reng][col]}`);
    }
}