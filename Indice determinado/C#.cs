using System;
using System.Collections.Generic;

class Program
{
    static void Main()
    {
        // Crear una lista con valores iniciales
        List<int> numeros = new List<int> { 10, 20, 30, 40, 50 };

        // Valor que se desea insertar
        int valorAInsertar = 25;

        // Índice en el que se insertará el valor
        int indice = 2;

        // Verificar si el índice es válido
        if (indice >= 0 && indice <= numeros.Count)
        {
            // Insertar el valor en la posición indicada
            numeros.Insert(indice, valorAInsertar);
        }
        else
        {
            Console.WriteLine("Índice fuera de rango.");
        }

        // Mostrar el contenido actualizado de la lista
        Console.Write("Lista actualizada: ");
        foreach (int num in numeros)
        {
            Console.Write(num + " ");
        }
        Console.WriteLine();
    }
}
