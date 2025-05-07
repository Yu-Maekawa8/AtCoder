/*
*Black jack   3枚のトランプの合計が　21以下なら win 22以上なら　bust  と出力する
*
*/


import java.util.*;

public class Main {
    public static void main(String[] args) {
        try (Scanner sc = new Scanner(System.in)) {
            int total = 0;
            for(int i = 0; i < 3; i++) {
                int tmp = sc.nextInt();
                total += tmp;
            }

            if(total >= 22) {
                System.out.println("bust");
            } else {
                System.out.println("win");
            }
        }
    }
}
