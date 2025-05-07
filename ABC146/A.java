/**
*次の日曜日まで何日か求める
*
*/

import java.util.*;

public class Main {
    public static void main(String[] args) {
        try (Scanner sc = new Scanner(System.in)) {
            String s = sc.next();
            String[] ar = {"SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"};

            System.out.println(ar.length - Arrays.asList(ar).indexOf(s));
        }
    }
}
