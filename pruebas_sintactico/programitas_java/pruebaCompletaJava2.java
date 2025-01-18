public class pruebaCompletaJava {
    public static void main(string[] args) {
        // Declaraciones de varios tipos de variables
        int a, b, j;
        float calif, pot, suma = 0.0f, sueldo, nsueldo;
        int categ = 2;
        b = a % 2;
        int h = 1;

        if (h != 9 ){
            system.out.println(" h es diferente de 9");
        }

        switch (categ) {
            case 1:
                b = 1;
                break;
            case 2:
                b = 2;
                break;
            default:
                b = 0;
        }

        float contador = 0.0f;
        for (int i = 0; i < 4; i++) {
           contador += 0.8f;
        }

        int i = 0;

        while (i < 4) {
            a-=1;
        }
        
        do {
            system.out.println("Teclea la calificacion ");
        } while (calif < 10);
        suma += 1;
        i++;
        
    }

    // Agregada una declaración de método
    public static void equisde() {
        system.out.println("Estamos en equisde");
        char x =  'z';
    }
}
