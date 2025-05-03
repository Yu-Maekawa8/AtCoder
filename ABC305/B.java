/**
 * 累積和の考え方の利用
 *ASCIIコード 'a' = 65 の利用
 */


import java.util.*;

public class Main {
    public static void main(String[] args) {
        try (Scanner sc = new Scanner(System.in)) {
            char ch1 = sc.next().charAt(0);
            char ch2 = sc.next().charAt(0);

            int[]ar = {0,3,4,8,9,14,23};

            System.out.println(Math.abs(ar[(int)ch1-65] - ar[(int)ch2-65]));

        }
    }
}
