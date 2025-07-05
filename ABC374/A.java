// AC済み問題: abc374_a
// 提出日時: 2024-10-20 14:44:52
// 実行時間: 66ms
// 注意: AtCoderは public class Main だが、IDE用に public class A に変更

package ABC374;

import java.util.*;
public class A{
    public static void main(String [] args){
        Scanner sc = new Scanner(System.in);
        String[] s = sc.nextLine().split("");        //点の数
        int n = s.length;
        
        if(s[n-3].equals("s") && s[n-2].equals("a") && s[n-1].equals("n")){
            System.out.println("Yes");
        }else{
            System.out.println("No");
        }
    }
}