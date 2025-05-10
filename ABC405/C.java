import java.util.*;
import java.math.*;

public class Main {
    public static void main(String[] args) {
        try (Scanner sc = new Scanner(System.in)) {
            int size = sc.nextInt();
            BigInteger[] a = new BigInteger[size];
            BigInteger[] sm = new BigInteger[size];
            BigInteger ans = BigInteger.ZERO;
            for (int i = 0; i < size; i++) {
                a[i] = sc.nextBigInteger();
            }
            
            sm[0] = a[0];
            for (int i = 0; i < size-1; i++) {
                sm[i+1] = sm[i].add(a[i+1]);
            }

            for (int i = 0; i < size-1; i++) {
                ans = ans.add((sm[size - 1].subtract(sm[i])).multiply(a[i]));

            }
            System.out.println(ans);
        }
    }
}
