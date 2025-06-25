// AC済み問題: abc162_b
// 提出日時: 2024-10-18 13:19:35
// 実行時間: 74ms
// 注意: AtCoderは public class Main だが、IDE用に public class B に変更

package ABC162;

import java.util.*;
public class B{
    public static void main(String[] args){
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        long total = 0;
        for(int i = 1 ; i <= n ; i++){
            if(i % 3 == 0 && i % 5 == 0){
                
            }else if(i % 3 == 0){
                
            }else if(i % 5 == 0){
              
            }else{
                total += i;
            }
        }
        System.out.println(total);
    }
}