// AC済み問題: abc373_a
// 提出日時: 2024-10-21 14:15:30
// 実行時間: 70ms
// 注意: AtCoderは public class Main だが、IDE用に public class A に変更

package ABC373;

import java.util.*;
public class A{
    public static void main(String [] args){
        Scanner sc = new Scanner(System.in);
        int len = 0;
        int count = 0;
        
        for(int i = 1 ; i <= 12 ; i++){
            String s = sc.nextLine();
            len = s.length();
            if(len == i){
              count++;
            }
        }
        System.out.println(count);
    }
}