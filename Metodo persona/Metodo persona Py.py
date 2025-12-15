class Persona:
    def __init__(self):
        self.nombre = input("Nombre: ")
        self.apellido = input("Apellido: ")
        self.sexo = input("Sexo (M/F): ")
        self.edad = self._pedir_edad()

    def _pedir_edad(self):
        while True:
            try:
                return int(input("Edad: "))
            except ValueError:
                print("Edad inválida. Intenta de nuevo.")

    def mostrar_datos(self):
        print(f"""
=== DATOS DE LA PERSONA ===
Nombre: {self.nombre}
Apellido: {self.apellido}
Sexo: {self.sexo}
Edad: {self.edad} años
============================
""")


def main():
    print("SISTEMA DE REGISTRO DE PERSONAS")
    try:
        N = int(input("¿Cuántas personas deseas registrar? "))
    except ValueError:
        print("Entrada inválida. Se registrarán 2 personas por defecto.")
        N = 2

    personas = [Persona() for _ in range(N)]

    print("\nRegistro completado exitosamente!\n")
    for i, persona in enumerate(personas, start=1):
        print(f"Persona {i}:")
        persona.mostrar_datos()


