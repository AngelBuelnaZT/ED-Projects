using System;

class Program
{
    static void Main()
    {
        // Crear el arreglo
        int[] arreglo = { 12, 45, 23, 67, 89, 34 };
        int tamaño = arreglo.Length;
        int valorBuscado = 67;
        bool encontrado = false;

        // Búsqueda del valor
        for (int i = 0; i < tamaño; i++)
        {
            if (arreglo[i] == valorBuscado)
            {
                Console.WriteLine("Valor encontrado en el índice " + i);
                encontrado = true;
                break;
            }
        }

        // Si no se encontró
        if (!encontrado)
        {
            Console.WriteLine("Valor no encontrado en el arreglo.");
        }
    }
}
