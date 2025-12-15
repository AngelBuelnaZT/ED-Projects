#include <iostream>
#include <string>

using namespace std;

int main() {
    // Definir una matriz de 3x3
    int tabla[3][3] = {
        {1, 2, 3},
        {4, 5, 6},
        {7, 8, 9}
    };

    cout << "Visualización de la matriz original:" << endl;
    // Imprimir la matriz inicial
    for (int renglon = 0; renglon < 3; renglon++) {
        string linea = "";
        for (int posicion = 0; posicion < 3; posicion++) {
            linea += to_string(tabla[renglon][posicion]) + "  ";
        }
        cout << linea << endl;
    }

    cout << "\nExploración por columnas:" << endl;
    // Recorrer la matriz por columnas
    for (int col = 0; col < 3; col++) {
        string datosColumna = "Columna " + to_string(col + 1) + ": ";
        for (int reng = 0; reng < 3; reng++) {
            datosColumna += to_string(tabla[reng][col]) + "  ";
        }
        cout << datosColumna << endl;
    }

    cout << "\nDetalles de elementos por columna:" << endl;
    // Mostrar cada elemento individualmente por columna
    for (int col = 0; col < 3; col++) {
        for (int reng = 0; reng < 3; reng++) {
            cout << "Valor en posición [" << reng << "," << col << "] = " << tabla[reng][col] << endl;
        }
    }

    return 0;
}