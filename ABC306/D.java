/*
 * 食べた料理の最大幸福度を求める問題
 * 
 * 動的計画法
 * 
 */

import java.util.*;
import java.math.*;

public class Main {
    public static void main(String[] args) {
        try (Scanner sc = new Scanner(System.in)) {
            int n = sc.nextInt();
            long[][] dp = new long[n + 1][2];
            long[] pis = new long[n];
            long[] hap = new long[n];

            for(int i = 0 ; i < n ; i++){
                pis[i] = sc.nextLong();
                hap[i] = sc.nextLong();
            }
            for (int i = 0; i < n; i++) {
                dp[i][0] =Long.MIN_VALUE / 2; // 安全な最小値の設定(Long.MIN.VALUE はdouble型のため /2をして小数点以下切り捨てている)
                dp[i][1] =Long.MIN_VALUE / 2; // 安全な最小値の設定(同様)
            }

            dp[0][0] = 0;　　　　　　　　//初期は毒はかかっていない

          /*
             *
             *現在までの最大満福度から料理を食べることで最大満腹度を更新するかどうか
             *
             * pis[i]が 0  == 解毒剤入りの料理を食べた とき
             * 
             * １、お腹を壊していない状態のときとお腹を壊した状態のときで幸福度が大きい方を選ぶ
             * ２、食べた後の幸福度を足し、直前の最大幸福度と比較して大きい方を選ぶ
             * ３、選んだものが次の状態のお腹を壊していない時の最大幸福度になる
             * 
             * pis[i]が 1 == 毒入りの料理を食べた とき
             * (制約：お腹を壊している状態で毒入り料理は食べると死ぬため、候補に入れない)
             * 
             * １、現在までのお腹を壊していない状態での最大満福度から料理を食べることで最大満腹度を更新するかどうか
             * ２、食べないなら、お腹を壊した状態の最大満福度を選ぶ
             */


            for (int i = 0; i < n; i++) {
                //pis[i]が 0  == 解毒剤入りの料理を食べた
                if(pis[i] == 0){
                    dp[i+1][0] = Math.max(dp[i][0],Math.max(dp[i][0], dp[i][1])+hap[i]);  
                //pis[i]が 1 == 毒入りの料理を食べた
                }else{
                    dp[i+1][1] = Math.max(dp[i][1], dp[i][0]+hap[i]);   
                }
                //食べない
                dp[i+1][0] = Math.max(dp[i+1][0], dp[i][0]);
                dp[i+1][1] = Math.max(dp[i+1][1], dp[i][1]);
                    
            }

            System.out.println(Math.max(dp[n][0], dp[n][1]));

        }
    }
}
