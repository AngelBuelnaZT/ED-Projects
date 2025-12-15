public class main {
    
    public static void main(String[] args) {
    
        int[] valores = {10, 20, 30, 40, 50, 60};
        
 
        valores[2] = 290;
        
        // Mostrar todo el contenido del arreglo 
        System.out.println("Contenido del arreglo:");
        for (int i = 0; i < valores.length; i++) {  
     
            System.out.println("valores[" + i + "] = " + valores[i]);
        }
    
        int suma = valores[0] + valores[2];
        
        System.out.println("\nSuma de elementos: " + suma);
    }
}