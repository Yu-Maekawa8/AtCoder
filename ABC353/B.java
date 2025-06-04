import java.util.*;
import java.math.*;

public class Main {
    public static void main(String[] args) {
        try (Scanner sc = new Scanner(System.in)) {
            int n = sc.nextInt();
            int m = sc.nextInt();

            int[] ar = new int[n];
            for (int i = 0; i < ar.length; i++) {
                ar[i] = sc.nextInt();
            }
            int total = 0;
            int cnt = 0;
            for (int i = 0; i < ar.length; i++) {
                if(total + ar[i] >m){
                    cnt++;
                    i--;
                    total = 0;
                    continue;
                }
                total += ar[i];
                
            }
            System.out.println(cnt+1);
        }
    }
}
