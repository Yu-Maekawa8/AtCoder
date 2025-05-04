/* 0 と 1 からなる長さ 64 の数列 A が与えられる
* A0 × 2^0 + A1 × 2^1 + ... + A63 × 2^63 の値を求める
*BigInteger を使って、オーバーフローせず安全に扱う
*/

import java.util.*;
import java.math.*;

public class Main {
    public static void main(String[] args) {
        try (Scanner sc = new Scanner(System.in)) {
            long[] ar = new long[64];
            BigInteger ans = BigInteger.ZERO;
            for(int i = 0 ; i < ar.length ; i++){
                ar[i] = sc.nextLong();
            }

            for(int i = 0 ; i < ar.length ; i++){
                ans = ans.add(BigInteger.valueOf(ar[i]).multiply(BigInteger.valueOf(2).pow(i)));
            }

            System.out.println(ans);
        }
    }
}
