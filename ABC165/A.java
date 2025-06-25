// AC済み問題: abc165_a
// 提出日時: 2024-10-18 10:53:02
// 実行時間: 79ms
// 注意: AtCoderは public class Main だが、IDE用に public class A に変更

package ABC165;

import java.util.*;
public class A{
    public static void main(String[] args){
        int flag = 0;
        Scanner sc = new Scanner(System.in);
        int k = sc.nextInt();
        int a = sc.nextInt();
        int b = sc.nextInt();
        for(int temp = a ; temp<= b ; temp++){
            if(temp % k == 0){
                flag = 1;
                break;
            }
        }
        if(flag == 1){
            System.out.println("OK");
        }else{
            System.out.println("NG");
        }
        sc.close();
    }
}