import java.util.*;
import java.math.*;

public class Main {
    public static void main(String[] args) {
        try (Scanner sc = new Scanner(System.in)) {
           int n = sc.nextInt();
           int[] ar = new int[n];
           for (int i = 0; i < n; i++) {
               ar[i] = sc.nextInt();
           }

           for (int i = 1; i < ar.length; i++) {
                if(ar[0] < ar[i]){
                    System.out.println(i+1);
                    return;
                }
           }
           
           System.out.println(-1);
        }
    }
}
