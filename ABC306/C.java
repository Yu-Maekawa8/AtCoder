/**
 * 同じ数字が2回出てきたら、その地点でその数字を出力するプログラム
 * 入力は3*n個の整数(同じ数字が3回出てくる)
 * 
 * mapを使って、数字の出現回数をカウントする
 */

import java.util.*;
import java.math.*;

public class Main {
    public static void main(String[] args) {
        try (Scanner sc = new Scanner(System.in)) {
            Map<Integer, Integer> map = new HashMap<>();
            int n = sc.nextInt();

            for (int i = 0; i < 3*n; i++) {
                int tmp = sc.nextInt();
                map.put(tmp, map.getOrDefault(tmp, 0) + 1);
                if(map.get(tmp) == 2) {
                    System.out.print(tmp + " ");
                }
            }
        }
    }
}
