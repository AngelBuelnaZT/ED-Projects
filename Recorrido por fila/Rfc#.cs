using System;
using System.Linq;

class MatrixRowTraversal
{
    static void Main()
    {
        // Definir una matriz 3x3
        int[,] grid = {
            {1, 2, 3},
            {4, 5, 6},
            {7, 8, 9}
        };

        Console.WriteLine("Matriz original (3x3):");
        // Mostrar la matriz completa
        for (int row = 0; row < 3; row++)
        {
            string line = string.Join(" ", Enumerable.Range(0, 3).Select(col => grid[row, col].ToString()));
            Console.WriteLine(line);
        }

        Console.WriteLine("\nRecorrido por filas:");
        // Mostrar cada fila con sus elementos
        for (int i = 0; i < 3; i++)
        {
            string rowContent = $"Fila {i + 1}: {string.Join(" ", Enumerable.Range(0, 3).Select(col => grid[i, col].ToString()))}";
            Console.WriteLine(rowContent);
        }

        Console.WriteLine("\nElementos individuales por fila:");
        // Mostrar cada elemento con su posición
        for (int i = 0; i < 3; i++)
        {
            for (int j = 0; j < 3; j++)
            {
                Console.WriteLine($"Posición [{i},{j}] = {grid[i, j]}");
            }
        }
    }
}