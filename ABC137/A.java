// AC済み問題: abc137_a
// 提出日時: 2024-10-15 11:07:02
// 実行時間: 71ms
// 注意: AtCoderは public class Main だが、IDE用に public class A に変更

package ABC137;

import java.util.*;
    public class A{
      public static void main(String[] args){
        Scanner sc = new Scanner(System.in);
        int a = sc.nextInt();
        int b = sc.nextInt();
        
        int plus = a+b;
        int minus = a-b;
        int intersect = a*b;
        int m = Math.max(plus,minus);
        if(intersect > m){
            System.out.println(intersect);
        }else{
            System.out.println(m);
        }
      }
    }