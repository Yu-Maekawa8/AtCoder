import java.util.*;

public class Main {
    public static void main(String [] args) {
        try(Scanner sc = new Scanner(System.in)){
            long n = sc.nextLong();
            int m = sc.nextInt();

            long tol = 0;
            for(int i = 0 ; i <= m ; i++){
                if(tol + Math.pow(n, i) > 1e9){
                    System.out.println("inf");
                    return;
                }
                tol += Math.pow(n, i);
            }

            System.out.println(tol);

        }
    }
}
