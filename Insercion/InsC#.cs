using System;

class InsertionSortExample
{
    static void InsertionSort(int[] arr, int n)
    {
        for (int i = 1; i < n; i++)
        {
            int key = arr[i]; // Elemento a insertar
            int j = i - 1;    // Índice del último elemento de la porción ordenada

            // Desplazar elementos mayores hacia la derecha
            while (j >= 0 && arr[j] > key)
            {
                arr[j + 1] = arr[j];
                j--;
            }
            arr[j + 1] = key; // Insertar el elemento en la posición correcta
        }
    }

    static void PrintArray(int[] arr, int n)
    {
        for (int i = 0; i < n; i++)
        {
            Console.Write(arr[i] + " ");
        }
        Console.WriteLine();
    }

    static void Main()
    {
        int[] arr = { 64, 34, 25, 12, 22, 11, 90 };
        int n = arr.Length;

        Console.WriteLine("Arreglo original: ");
        PrintArray(arr, n);

        InsertionSort(arr, n);

        Console.WriteLine("Arreglo ordenado: ");
        PrintArray(arr, n);
    }
}