#include <iostream>
#include <string>
using namespace std;

class Persona {
private:
    string nombre;
    string apellido;
    string sexo;
    unsigned int edad;

public:

    Persona() : nombre(""), apellido(""), sexo(""), edad(0) {}

    // Método para pedir datos
    void PedirDatos() {
        cout << "\n=== INGRESO DE DATOS ===" << endl;

        cout << "Nombre: ";
        getline(cin, nombre);

        cout << "Apellido: ";
        getline(cin, apellido);

        cout << "Sexo (M/F): ";
        getline(cin, sexo);

        cout << "Edad: ";
        cin >> edad;
        cin.ignore(); 
    }

    // Método para mostrar datos
    void MostrarDatos() const {
        cout << "\n=== DATOS DE LA PERSONA ===" << endl;
        cout << "Nombre: " << nombre << endl;
        cout << "Apellido: " << apellido << endl;
        cout << "Sexo: " << sexo << endl;
        cout << "Edad: " << edad << " años" << endl;
        cout << "============================" << endl;
    }
};

int main() {
    const int N = 2;
    Persona* personas[N];

    cout << "SISTEMA DE REGISTRO DE PERSONAS" << endl;
    cout << "Ingrese los datos de " << N << " personas:" << endl;

    for (int i = 0; i < N; ++i) {
        cout << "\nPersona " << i + 1 << ":" << endl;
        personas[i] = new Persona();
        personas[i]->PedirDatos();
        personas[i]->MostrarDatos();
    }

    cout << "\nRegistro completado exitosamente!" << endl;


    for (int i = 0; i < N; ++i) {
        delete personas[i];
    }

    return 0;
}
