#include <iostream>
#include <cstdlib>
#include <ctime>

int bubble_sort(int arr[], int n) {
    int swap_counter = 0;
    bool swapped;
    
    do {
        swapped = false;
        for (int i = 1; i < n; ++i) {
            if (arr[i - 1] > arr[i]) {
                int temp = arr[i - 1];
                arr[i - 1] = arr[i];
                arr[i] = temp;
                swapped = true;
                ++swap_counter;
            }
        }
        --n;
    } while (swapped);
    
    return swap_counter;
}

int main() {
    const int SIZE = 15;
    int arr[SIZE];
    srand(time(0));
    
    // array con valores aleatorios
    cout << "Array original (valores aleatorios):\n";
    for (int i = 0; i < SIZE; ++i) {
        arr[i] = rand() % 100 + 1; 
        cout << arr[i] << " ";
    }
    cout << "\n";
    int swap_counter = bubble_sort(arr, SIZE);
    cout << "\nArray ordenado:\n";
    for (int i = 0; i < SIZE; ++i) {
        cout << arr[i] << " ";
    }
    
    cout << "\n\nTotal de intercambios realizados: " << swap_counter << "\n";
    
    return 0;
}