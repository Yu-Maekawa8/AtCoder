// AC済み問題: abc376_a
// 提出日時: 2024-10-19 21:48:09
// 実行時間: 73ms
// 注意: AtCoderは public class Main だが、IDE用に public class A に変更

package ABC376;

import java.util.*;
public class A{
    public static void main(String [] args){
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int c = sc.nextInt();
        int firstt = sc.nextInt();
        int count = 1;
        int answer = 1;
        
        while(count < n){
            int t1 = sc.nextInt();
            int checkvalue = t1 - firstt;
            count++;
            if(checkvalue >= c){
                answer++;
                firstt = t1;
            }
        }
        System.out.println(answer);
    }
}