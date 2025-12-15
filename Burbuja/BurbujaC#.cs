using System;

class Program
{
    static int BubbleSort(int[] arr, int n)
    {
        int swapCounter = 0;
        bool swapped;

        do
        {
            swapped = false;
            for (int i = 1; i < n; ++i)
            {
                if (arr[i - 1] > arr[i])
                {
                    int temp = arr[i - 1];
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

    static void Main(string[] args)
    {
        const int SIZE = 15;
        int[] arr = new int[SIZE];
        Random rand = new Random();

        Console.WriteLine("Array original (valores aleatorios):");
        for (int i = 0; i < SIZE; ++i)
        {
            arr[i] = rand.Next(1, 101); // 1 to 100
            Console.Write(arr[i] + " ");
        }
        Console.WriteLine();

        int swapCounter = BubbleSort(arr, SIZE);

        Console.WriteLine("\nArray ordenado:");
        for (int i = 0; i < SIZE; ++i)
        {
            Console.Write(arr[i] + " ");
        }

        Console.WriteLine("\n\nTotal de intercambios realizados: " + swapCounter);
    }
}