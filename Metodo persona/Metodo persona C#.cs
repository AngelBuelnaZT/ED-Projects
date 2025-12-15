C#

using System;

public class Persona
{
   
    private string nombre;
    private string apellido;
    private string sexo;
    private uint edad;

   
    public Persona()
    {
        nombre = "";
        apellido = "";
        sexo = "";
        edad = 0;
    }

 
    public void PedirDatos()
    {
        Console.WriteLine("\n=== INGRESO DE DATOS ===");
        
        Console.Write("Nombre: ");
        nombre = Console.ReadLine();

        Console.Write("Apellido: ");
        apellido = Console.ReadLine();

        Console.Write("Sexo (M/F): ");
        sexo = Console.ReadLine();

        Console.Write("Edad: ");
        edad = Convert.ToUInt32(Console.ReadLine());
    }

  
    public void MostrarDatos()
    {
        Console.WriteLine("\n=== DATOS DE LA PERSONA ===");
        Console.WriteLine($"Nombre: {nombre}");
        Console.WriteLine($"Apellido: {apellido}");
        Console.WriteLine($"Sexo: {sexo}");
        Console.WriteLine($"Edad: {edad} años");
        Console.WriteLine("============================");
    }
}

public class Program
{
    public static void Main(string[] args)
    {
        Persona[] personas = new Persona[2];

        Console.WriteLine("SISTEMA DE REGISTRO DE PERSONAS");
        Console.WriteLine("Ingrese los datos de 2 personas:");

        // Pedir y mostrar datos
        for (int i = 0; i < 2; i++)
        {
            Console.WriteLine($"\nPersona {i + 1}:");
            personas[i] = new Persona();
            personas[i].PedirDatos();
            personas[i].MostrarDatos();
        }

        Console.WriteLine("\nRegistro completado exitosamente!");
    }
}