/*
* 数字は広義単調増加で、100<=x<=675　かつ　25の倍数なら　Yes　と出力する
*
*
*/


import java.util.*;
import java.math.*;

public class Main {
    public static void main(String[] args) {
        try (Scanner sc = new Scanner(System.in)) {
            int std = 0;
            for (int i = 0; i < 8; i++) {
                int tmp = sc.nextInt();
                if(std <= tmp && tmp >= 100 && tmp <= 675 && tmp % 25 == 0){
                    std = tmp;
                }else{
                    System.out.println("No");
                    return;
                }
            }
            System.out.println("Yes");
        }
    }
}
