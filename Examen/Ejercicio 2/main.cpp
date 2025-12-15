#include <iostream>
#include <vector>

using namespace std;

int main() {
    int rows, cols;
    cout << "Ingrese el numero de filas: ";
    cin >> rows;
    cout << "Ingrese el numero de columnas: ";
    cin >> cols;
    vector<vector<int> > matrix(rows, vector<int>(cols));
    cout << "Ingrese los elementos de la matriz ( " << rows << "x" << cols << "): ";
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            cin >> matrix[i][j];
        }
    }
    int maxVal = matrix[0][0];
    int maxRow = 0, maxCol = 0;
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            if (matrix[i][j] > maxVal) {
                maxVal = matrix[i][j];
                maxRow = i;
                maxCol = j;
            }
        }
    }

    cout << "Valor maximo: " << maxVal << " en la posicion (" << maxRow << ", " << maxCol << ")" << endl;

    return 0;
}
