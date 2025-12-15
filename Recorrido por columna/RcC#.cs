
class Program
{
    static void Main()
    {
        // Definir una matriz de 3x3
        int[,] tabla = {
            {1, 2, 3},
            {4, 5, 6},
            {7, 8, 9}
        };

        Console.WriteLine("Visualización de la matriz original:");
        // Imprimir la matriz inicial
        for (int renglon = 0; renglon < 3; renglon++)
        {
            string linea = "";
            for (int posicion = 0; posicion < 3; posicion++)
            {
                linea += tabla[renglon, posicion] + "  ";
            }
            Console.WriteLine(linea);
        }

        Console.WriteLine("\nExploración por columnas:");
        // Recorrer la matriz por columnas
        for (int col = 0; col < 3; col++)
        {
            string datosColumna = $"Columna {col + 1}: ";
            for (int reng = 0; reng < 3; reng++)
            {
                datosColumna += tabla[reng, col] + "  ";
            }
            Console.WriteLine(datosColumna);
        }

        Console.WriteLine("\nDetalles de elementos por columna:");
        // Mostrar cada elemento individualmente por columna
        for (int col = 0; col < 3; col++)
        {
            for (int reng = 0; reng < 3; reng++)
            {
                Console.WriteLine($"Valor en posición [{reng},{col}] = {tabla[reng, col]}");
            }
        }
    }
}