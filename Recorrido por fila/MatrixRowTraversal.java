public class MatrixRowTraversal {
    public static void main(String[] args) {
        // Definir una matriz 3x3
        int[][] grid = {
            {1, 2, 3},
            {4, 5, 6},
            {7, 8, 9}
        };

        System.out.println("Matriz original (3x3):");
        // Mostrar la matriz completa
        for (int row = 0; row < 3; row++) {
            String line = String.join(" ", new String[] {
                String.valueOf(grid[row][0]),
                String.valueOf(grid[row][1]),
                String.valueOf(grid[row][2])
            });
            System.out.println(line);
        }

        System.out.println("\nRecorrido por filas:");
        // Mostrar cada fila con sus elementos
        for (int i = 0; i < 3; i++) {
            String rowContent = "Fila " + (i + 1) + ": " + String.join(" ", new String[] {
                String.valueOf(grid[i][0]),
                String.valueOf(grid[i][1]),
                String.valueOf(grid[i][2])
            });
            System.out.println(rowContent);
        }

        System.out.println("\nElementos individuales por fila:");
        // Mostrar cada elemento con su posición
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                System.out.println("Posición [" + i + "," + j + "] = " + grid[i][j]);
            }
        }
    }
}