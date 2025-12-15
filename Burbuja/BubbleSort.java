import java.util.Random;

public class BubbleSort {
    static int bubbleSort(int[] arr, int n) {
        int swapCounter = 0;
        boolean swapped;

        do {
            swapped = false;
            for (int i = 1; i < n; ++i) {
                if (arr[i - 1] > arr[i]) {
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

    public static void main(String[] args) {
        final int SIZE = 15;
        int[] arr = new int[SIZE];
        Random rand = new Random();

        System.out.println("Array original (valores aleatorios):");
        for (int i = 0; i < SIZE; ++i) {
            arr[i] = rand.nextInt(100) + 1; // 1 to 100
            System.out.print(arr[i] + " ");
        }
        System.out.println();

        int swapCounter = bubbleSort(arr, SIZE);

        System.out.println("\nArray ordenado:");
        for (int i = 0; i < SIZE; ++i) {
            System.out.print(arr[i] + " ");
        }

        System.out.println("\n\nTotal de intercambios realizados: " + swapCounter);
    }
}