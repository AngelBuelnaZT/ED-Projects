#include <iostream>
#include <vector>

int main() {
    std::vector<int> numeros = {10, 20, 30, 40, 50};
    int valorAInsertar = 25;
    int indice = 2; 

    if (indice >= 0 && indice <= numeros.size()) {
        numeros.insert(numeros.begin() + indice, valorAInsertar);
    } else {
        std::cout << "Índice fuera de rango." << std::endl;
    }

    std::cout << "Vector actualizado: ";
    for (int num : numeros) {
        std::cout << num << " ";
    }
    std::cout << std::endl;

    return 0;
}