public class SelectionSort {
    static void selectionSort(int[] arr, int n) {
        for (int i = 0; i < n - 1; i++) {
            int minIndex = i; // Índice del mínimo actual

            // Buscar el mínimo en el resto del arreglo
            for (int j = i + 1; j < n; j++) {
                if (arr[j] < arr[minIndex]) {
                    minIndex = j;
                }
            }

            // Intercambiar el mínimo con el elemento en i
            if (minIndex != i) {
                int temp = arr[i];
                arr[i] = arr[minIndex];
                arr[minIndex] = temp;
            }
        }
    }

    static void printArray(int[] arr, int n) {
        for (int i = 0; i < n; i++) {
            System.out.print(arr[i] + " ");
        }
        System.out.println();
    }

    public static void main(String[] args) {
        int[] arr = {64, 34, 25, 12, 22, 11, 90};
        int n = arr.length;

        System.out.print("Arreglo original: ");
        printArray(arr, n);

        selectionSort(arr, n);

        System.out.print("Arreglo ordenado: ");
        printArray(arr, n);
    }
}