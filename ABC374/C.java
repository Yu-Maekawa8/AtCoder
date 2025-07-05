// AC済み問題: abc374_c
// 提出日時: 2024-10-22 00:14:19
// 実行時間: 175ms
// 注意: AtCoderは public class Main だが、IDE用に public class C に変更

package ABC374;

import java.util.*;
public class C{
    public static void main(String [] args){
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int[] number = new int[n];
        int atotal = 0;
        int btotal = 0;
        int ans = Integer.MAX_VALUE;
        
        for(int i = 0 ; i < n ; i++){ //配列格納
          number[i] = sc.nextInt();
        }
        
        for(int i = 0 ; i < (1<<n) ; i++){
            atotal = 0;
            btotal = 0;
            for(int j = 0 ; j < n ; j++){
              if((1 & i >> j) == 1){
                atotal += number[j];
              }else{
                btotal += number[j];
              }
            }
            int maxN = Math.max(atotal,btotal);
            ans = Math.min(maxN,ans);
        }
        System.out.println(ans);
    }
}