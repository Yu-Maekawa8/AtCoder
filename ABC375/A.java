// AC済み問題: abc375_a
// 提出日時: 2024-10-19 23:20:55
// 実行時間: 215ms
// 注意: AtCoderは public class Main だが、IDE用に public class A に変更

package ABC375;

import java.util.*;
public class A{
    public static void main(String [] args){
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        sc.nextLine();
        String[] s = sc.nextLine().split("");
        int count =0;
        
        for(int i =1 ; i < n-1 ; i++){
          if(s[i].equals(".") && s[i - 1].equals("#") && s[i + 1].equals("#")){
            count++;
          }
        }
        System.out.println(count);
    }
}