import java.util.*;

public class Main {
    public static void main(String [] args) {
        try(Scanner sc = new Scanner(System.in)){
            int n = sc.nextInt();
            int ans = 400 % n == 0 ? 400/n : -1;
            System.out.println(ans);
        }
    }
}