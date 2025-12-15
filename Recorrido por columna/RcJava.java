public class MatrixTraversal {
    public static void main(String[] args) {
        // Definir una matriz de 3x3
        int[][] tabla = {
            {1, 2, 3},
            {4, 5, 6},
            {7, 8, 9}
        };

        System.out.println("Visualización de la matriz original:");
        // Imprimir la matriz inicial
        for (int renglon = 0; renglon < 3; renglon++) {
            String linea = "";
            for (int posicion = 0; posicion < 3; posicion++) {
                linea += tabla[renglon][posicion] + "  ";
            }
            System.out.println(linea);
        }

        System.out.println("\nExploración por columnas:");
        // Recorrer la matriz por columnas
        for (int col = 0; col < 3; col++) {
            String datosColumna = "Columna " + (col + 1) + ": ";
            for (int reng = 0; reng < 3; reng++) {
                datosColumna += tabla[reng][col] + "  ";
            }
            System.out.println(datosColumna);
        }

        System.out.println("\nDetalles de elementos por columna:");
        // Mostrar cada elemento individualmente por columna
        for (int col = 0; col < 3; col++) {
            for (int reng = 0; reng < 3; reng++) {
                System.out.println("Valor en posición [" + reng + "," + col + "] = " + tabla[reng][col]);
            }
        }
    }
}