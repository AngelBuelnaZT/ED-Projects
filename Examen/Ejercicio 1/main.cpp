#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int BusBi(const vector<int>& arr, int obj) {
    int iz = 0, der = arr.size() - 1;
    while (iz <= der) {
    int mid = iz + (der - iz) / 2;
    if (arr[mid] == obj) return mid;
    if (arr[mid] < obj) iz = mid + 1;
    else iz = mid - 1;
    }
    return -1;
}
int main() {
    int size = 10;
    vector<int> arr(size);
    cout << "Ingrese " << size << " elementos: ";
    for(int i = 0; i < size; ++i) {
        cin >> arr[i];
    }
    sort(arr.begin(), arr.end());
    cout << "Arreglo ordenado: ";
    for (int num : arr) {
    cout << num << " ";
    cout << endl;
    int obj;
    cout << "Ingrese el valor a buscar: ";
     cin >> obj;
    int resul = BusBi(arr,obj);
    if (resul != -1) {
       cout << "Valor encontrado en la posicion: " << resul << endl;
    } else {
        cout << "Valor no encontrado." << endl;
    }
    return 0;
}

}
