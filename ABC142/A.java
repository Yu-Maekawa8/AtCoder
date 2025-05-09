/*
*
* d以下の自然数で一つ自然数を選ぶときの奇数の確率
*
*
*/

import java.util.*;

public class Main {
    public static void main(String[] args) {
        try (Scanner sc = new Scanner(System.in)) {
            double d = sc.nextDouble();
            double cnt = d % 2;

            System.out.println(((d/2)+cnt)/d);

        }
    }
}
