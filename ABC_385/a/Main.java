import java.util.*;

public class Main {
    public static void main(String [] args) {
        try(Scanner sc = new Scanner(System.in)){
            int a = sc.nextInt(), b = sc.nextInt(),c = sc.nextInt();

            String ans = a == b&& b == c || (a + b) == c || (a + c) == b || (b + c) == a ? "Yes" : "No";
            System.out.println(ans);
        }
    }
}
