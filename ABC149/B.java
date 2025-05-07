/*
*
*
*/

package abc149;

import java.util.*;

public class Main {
    public static void main(String[] args) {
        try (Scanner sc = new Scanner(System.in)) {
            long in1 = sc.nextLong();
            long in2 = sc.nextLong();
            long k = sc.nextLong();
            long rem1 = in1;
            long rem2 = in2;

            rem1 = in1 <= k ? 0 : in1-k;
            k = k - in1;
            if(rem1 == 0 && k >0) rem2 = in2 <= k ? 0 :in2 -k;




            System.out.println(rem1 + " " + rem2);

        }
    }
}
