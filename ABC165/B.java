// AC済み問題: abc165_b
// 提出日時: 2024-10-18 13:47:25
// 実行時間: 72ms
// 注意: AtCoderは public class Main だが、IDE用に public class B に変更

package ABC165;

import java.util.*;
public class B{
    public static void main(String[] args){
        Scanner sc = new Scanner(System.in);
        long x = sc.nextLong();
        long price =100;
        int i = 0;
        
        while(price < x){
            i++;
            price += price/100; 
        }
        System.out.println(i);
    }
}