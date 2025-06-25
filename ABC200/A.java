// AC済み問題: abc200_a
// 提出日時: 2024-10-18 19:06:31
// 実行時間: 73ms
// 注意: AtCoderは public class Main だが、IDE用に public class A に変更

package ABC200;

import java.util.*;
public class A{
    public static void main(String[] args){
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        
        if(n % 100 == 0){
            System.out.println(n/100);
        }else{
            System.out.println(n/100+1);
        }
    }
}