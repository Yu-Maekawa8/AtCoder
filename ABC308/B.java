/**
*皿ごとの値段を与えられ、　合計金額を出力
*
*
*/


import java.util.*;
import java.math.*;

public class Main {
    public static void main(String[] args) {
        try (Scanner sc = new Scanner(System.in)) {
            int n = sc.nextInt();
            int m = sc.nextInt();
            int total = 0;

            String[] s = new String[n];
            String[] t = new String[m];
            int[] price = new int[m+1];
            for(int i = 0; i < n; i++) {
                s[i] = sc.next();
            }
            for(int i = 0; i < m; i++) {
                t[i] = sc.next();
            }

            for(int i = 0; i < m+1; i++) {
                price[i] = sc.nextInt();
            }

            for(int i = 0 ; i < n ; i++) {
                for(int j = 0 ; j < m ; j++) {
                    if(s[i].equals(t[j])) {
                        total += price[j+1];
                        break;
                    }else if(j == m-1) {
                        total += price[0];
                    }
                }
            }
            System.out.println(total);

        }
    }
}
