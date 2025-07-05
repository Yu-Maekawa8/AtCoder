// AC済み問題: abc369_a
// 提出日時: 2024-11-22 20:05:37
// 実行時間: 70ms
// 注意: AtCoderは public class Main だが、IDE用に public class A に変更

package ABC369;

import java.util.*;

public class A {
    public static void main(String [] args) {
        try(Scanner sc = new Scanner(System.in)){
            int a = sc.nextInt(),b = sc.nextInt();

            System.out.println(Math.abs(a-b) % 2 == 1 ? 2 :Math.abs(a-b) == 0 ? 1: 3);
        }
    }
}