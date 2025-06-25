import java.util.*;

public class Main {
    public static void main(String[] args) {
        try (Scanner sc = new Scanner(System.in)) {
            int n = sc.nextInt();
            int idx = 0;
        
            String[] ar = new String[n];
            int[] ar2 = new int[n];
            for (int i = 0; i < n; i++) {
                ar[i] = sc.next();
                ar2[i] = sc.nextInt();
            }
            
            int min = Integer.MAX_VALUE;

            for(int i = 0; i < n; i++) {
                if (min > ar2[i]) {
                    min = ar2[i];
                    idx = i;
                    
                }
            }
            for(int i = 0 ; i < n; i++) {
                System.out.println(ar[idx % n] + " ");
                idx++;
            }
        }
    }
}
