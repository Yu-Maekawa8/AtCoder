/*
*1週間ごとの歩数合計を出力する
*/

import java.util.*;
import java.math.*;

public class Main {
    public static void main(String[] args) {
        try (Scanner sc = new Scanner(System.in)) {
            int size = sc.nextInt();
            int total = 0;
            int[] ar = new int[7*size];
            for (int i = 0; i < 7*size; i++) {
                ar[i] = sc.nextInt();
            }

            for(int day = 0 ; day < 7*size ; day++){
                total += ar[day];
                if((day+1) % 7 == 0 ){
                    System.out.print(total + " ");
                    total = 0;
                }
            }
        }
    }
}
