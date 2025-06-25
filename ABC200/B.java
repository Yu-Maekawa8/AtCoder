// AC済み問題: abc200_b
// 提出日時: 2024-10-18 19:17:59
// 実行時間: 74ms
// 注意: AtCoderは public class Main だが、IDE用に public class B に変更

package ABC200;

import java.util.*;
public class B{
    public static void main(String[] args){
        Scanner sc = new Scanner(System.in);
        long n = sc.nextInt();
        int k = sc.nextInt();
        
        for(int i = 1 ; i <= k ; i++){
            if(n % 200 == 0){
                n = n/200;
            }else{
                n = n*1000+200;
            }
        }
        System.out.println(n);
    }
}