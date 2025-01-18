
import java.util.Scanner;
public class pruebaCompletaFinal {
    public static void main(String[] args) {
        // Declaraciones de varios tipos de variables
        int a, b;
        /* Comentario
           de bloque */
        int[] vec = new int[10];
        int categ = 2;
        float [] vecFloat = {2.3f, 5.0f, 3.1f};
        float sueldo;
        Scanner scanner = new Scanner(System.in);
        
        System.out.println("Teclea un numero:");
        a = scanner.nextInt();
        b = a % 2;
        if (b == 0) {
            System.out.println(a + " el numero es ");
        }

        float nsueldo = 0;
        switch (categ) {
            case 1:
                nsueldo = sueldo * 1.15f;
                break;
            case 2:
                nsueldo = sueldo * 1.10f;
                break;
        }

        int n = 0;
        int pot, suma = 0;
        for (int i = 0; i <= n; i++) {
            pot = 1;
            for (int j = 0; j < i; j++) {
                pot = pot * 2;
            }
            suma = suma + 1 / pot;
        }

        int i = 0;
        float calif = 0;
        while (i <= 4) {
            do {
                System.out.printf("Teclea la calificacion %d:", i);
                calif = scanner.nextFloat();
            } while (calif < 0 || calif > 10);
            suma += calif;
            i++;
        }
    }

    public static float suma(float a, float b) {
        return a + b;
    }
}
