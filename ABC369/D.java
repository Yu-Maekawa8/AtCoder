// AC済み問題: abc369_d
// 提出日時: 2024-11-22 00:25:53
// 実行時間: 499ms
// 注意: AtCoderは public class Main だが、IDE用に public class D に変更

package ABC369;

import java.util.*;

public class D {
    public static void main(String [] args) {
        try(Scanner sc = new Scanner(System.in)){
            int n = sc.nextInt();
            long ans = 0;
            long[] s = new long[n];
            for(int i = 0 ; i<n ; i++){
                s[i] = sc.nextLong();
            }
            long[][] dp =new long[n+1][2];
            for(int i = 0 ; i < n ; i++){
                dp[i][0] = -999999999999l;
                dp[i][1] = -999999999999l;
            }
            dp[0][1] = 0;
            for(int i = 0 ; i < n ;i++){
                int nexti = i+1;
                for(int j = 0 ; j < 2 ; j++){
                   { //カウントする場合
                    int nextj = j^1;   //交差
                    long xp = (j % 2 == 0) ? s[i]*2 : s[i];
                    dp[nexti][nextj] = Math.max(dp[nexti][nextj] , dp[i][j]+xp);
                    }
                    {//カウントしない場合
                    int nextj  = j;    //直進
                    dp[nexti][nextj] = Math.max(dp[nexti][nextj] , dp[i][j]);
                    }
                }
            }
            ans = Math.max(dp[n][0], dp[n][1]);
            System.out.println(ans);
        }

    }

    public static void swap(Object[] a ,int i ,int j) {
        Object tmp = a[i];
        a[i] = a[j];
        a[j] = tmp;
    }
}