#include <iostream>
#include <string>

using namespace std;

int main() {
    // Definir una matriz 3x3
    int grid[3][3] = {
        {1, 2, 3},
        {4, 5, 6},
        {7, 8, 9}
    };

    cout << "Matriz original (3x3):" << endl;
    // Mostrar la matriz completa
    for (int row = 0; row < 3; row++) {
        string line = "";
        for (int col = 0; col < 3; col++) {
            line += to_string(grid[row][col]) + " ";
        }
        cout << line << endl;
    }

    cout << "\nRecorrido por filas:" << endl;
    // Mostrar cada fila con sus elementos
    for (int i = 0; i < 3; i++) {
        string rowContent = "Fila " + to_string(i + 1) + ": ";
        for (int col = 0; col < 3; col++) {
            rowContent += to_string(grid[i][col]) + " ";
        }
        cout << rowContent << endl;
    }

    cout << "\nElementos individuales por fila:" << endl;
    // Mostrar cada elemento con su posición
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            cout << "Posición [" << i << "," << j << "] = " << grid[i][j] << endl;
        }
    }

    return 0;
}