
let numeros = [10, 20, 30, 40, 50];

let valorAInsertar = 25;

// Índice en el que se insertará el valor
let indice = 2;

// Verificar si el índice es válido
if (indice >= 0 && indice <= numeros.length) {
    // Insertar el valor usando splice
    numeros.splice(indice, 0, valorAInsertar);
} else {
    console.log("Índice fuera de rango.");
}

// Mostrar el contenido actualizado del arreglo
console.log("Arreglo actualizado:", numeros);
