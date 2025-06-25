// AC済み問題: abc164_a
// 提出日時: 2024-10-18 19:32:36
// 実行時間: 74ms
// 注意: AtCoderは public class Main だが、IDE用に public class A に変更

package ABC164;

import java.util.*;
public class A{
    public static void main(String [] args){
        Scanner sc = new Scanner(System.in);
        int s = sc.nextInt();
        int w = sc.nextInt();
        
        if(s<=w){
            System.out.println("unsafe");
        }else{
            System.out.println("safe");
        }
    }
}