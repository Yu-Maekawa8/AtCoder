/*
* 九九の計算だけは出来る！！
*※10の段以上はできない　＝＞-1となる
*
*/

import java.util.*;

public class Main {
    public static void main(String[] args) {
        try (Scanner sc = new Scanner(System.in)) {
            int a = sc.nextInt(), b = sc.nextInt();

            if(a > 9 || b > 9){
                System.out.println(-1);
                return;
            }

            System.out.println(a*b);

        }
    }
}
