import java.util.*;
import java.math.*;

public class Main {
    public static void main(String[] args) {
        try (Scanner sc = new Scanner(System.in)) {
            int n = sc.nextInt();
            int m = sc.nextInt();

            int[] ar = new int[n];
            int[] cnt = new int[m];

            for (int i = 0; i < n; i++) {
                ar[i] = sc.nextInt();
            }

            for(int i = 0; i < n; i++) {
                cnt[ar[i]-1]++;
            }
            for(int i = 0; i < m; i++) {
                if(cnt[i] == 0) {
                    System.out.println(0);
                    return;
                }
            }
            int ans = 0;
            for(int i = 0; i < n; i++) {
                cnt[ar[ar.length-1-i]-1]--;
                ans++;
                if(cnt[ar[ar.length-1-i]-1] == 0) {
                    System.out.println(ans);
                    return;
                } 
            }


        }
    }
}
