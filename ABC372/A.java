// AC済み問題: abc372_a
// 提出日時: 2024-10-21 16:24:51
// 実行時間: 76ms
// 注意: AtCoderは public class Main だが、IDE用に public class A に変更

package ABC372;

import java.util.*;
public class A{
    public static void main(String [] args){
        Scanner sc = new Scanner(System.in);
        String[] s = sc.nextLine().split("");
        int len = s.length;
        
        for(int i = 0 ; i < len ; i++){
          if(!s[i].equals(".")){
            System.out.print(s[i]);
          }
        }
        
    }
}