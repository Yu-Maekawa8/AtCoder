// AC済み問題: abc206_b
// 提出日時: 2024-10-18 13:29:56
// 実行時間: 71ms
// 注意: AtCoderは public class Main だが、IDE用に public class B に変更

package ABC206;

import java.util.*;
public class B{
    public static void main(String[] args){
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int total = 0;
        int i = 0;
        
        for(i = 1 ; i <= n ; i++){
            total += i;
            if(total >= n){
                break;
            }
        }
        System.out.println(i);
    }
}