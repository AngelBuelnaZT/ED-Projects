// Crear el arreglo
let arreglo = [12, 45, 23, 67, 89, 34];
let valorBuscado = 67;
let encontrado = false;

// Búsqueda del valor
for (let i = 0; i < arreglo.length; i++) {
    if (arreglo[i] === valorBuscado) {
        console.log("Valor encontrado en el índice " + i);
        encontrado = true;
        break;
    }
}

// Si no se encontró
if (!encontrado) {
    console.log("Valor no encontrado en el arreglo.");
}
