public class Main {
    public static void main(String[] args) {
        // Crear el arreglo
        int[] arreglo = {12, 45, 23, 67, 89, 34};
        int valorBuscado = 67;
        boolean encontrado = false;

        // Búsqueda del valor
        for (int i = 0; i < arreglo.length; i++) {
            if (arreglo[i] == valorBuscado) {
                System.out.println("Valor encontrado en el índice " + i);
                encontrado = true;
                break;
            }
        }

        // Si no se encontró
        if (!encontrado) {
            System.out.println("Valor no encontrado en el arreglo.");
        }
    }
}
