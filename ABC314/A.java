/*
* piを100桁格納し、Substringする
*/

import java.util.*;
import java.math.*;

public class Main {
    public static void main(String[] args) {
        try (Scanner sc = new Scanner(System.in)) {
            String pi = "3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679";
            int n = sc.nextInt();

            System.out.print(pi.substring(0,n+2));
        }
    }
}
