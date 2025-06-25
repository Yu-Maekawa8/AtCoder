// AC済み問題: abc153_a
// 提出日時: 2024-10-15 01:08:59
// 実行時間: 74ms
// 注意: AtCoderは public class Main だが、IDE用に public class A に変更

package ABC153;

import java.util.*;
    public class A{
      public static void main(String[] args){
        int count = 0;
        Scanner sc = new Scanner(System.in);
        int hp = sc.nextInt();
        int at = sc.nextInt();
        do{
            hp = hp - at;
            count++;
                
        }while(hp > 0);
        System.out.println(count);
      }
    }