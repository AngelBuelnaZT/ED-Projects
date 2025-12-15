import java.util.ArrayList;

public class Main {
    public static void main(String[] args) {
        // Crear una lista con valores iniciales
        ArrayList<Integer> numeros = new ArrayList<>();
        numeros.add(10);
        numeros.add(20);
        numeros.add(30);
        numeros.add(40);
        numeros.add(50);

        // Valor que se desea insertar
        int valorAInsertar = 25;

        // Índice en el que se insertará el valor
        int indice = 2;

        // Verificar si el índice es válido
        if (indice >= 0 && indice <= numeros.size()) {
            numeros.add(indice, valorAInsertar);
        } else {
            System.out.println("Índice fuera de rango.");
        }

        // Mostrar el contenido actualizado de la lista
        System.out.print("Lista actualizada: ");
        for (int num : numeros) {
            System.out.print(num + " ");
        }
        System.out.println();
    }
}
