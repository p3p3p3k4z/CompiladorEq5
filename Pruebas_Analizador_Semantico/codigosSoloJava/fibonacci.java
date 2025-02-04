import java.util.ArrayList;
import java.util.List;

public class Fibonacci {
    public static List<Integer> fibonacci(int n) {
        List<Integer> sequence = new ArrayList<>();
        int a = 0, b = 1;
        while (sequence.size() < n) {
            sequence.add(a);
            int next = a + b;
            a = b;
            b = next;
        }
        return sequence;
    }

    public static void main(String[] args) {
        int numTerms = 50; 
        List<Integer> sequence = fibonacci(numTerms);
        System.out.println(sequence);
    }
}
