/*
* 与えられた文字列の長さを 長さｎから２ｎにする
*ex. atcoder => aattccooddeerr
*/


import java.util.*;

public class Main {
    public static void main(String[] args) {
        try (Scanner sc = new Scanner(System.in)) {
            int n = sc.nextInt();
            String s = sc.next();
            StringBuilder sb = new StringBuilder();

            for(int i = 0 ; i < n ; i++){
                for (int j = 0; j < 2; j++) {
                    sb.append(s.charAt(i));
                }
            }

            System.out.println(sb.toString());
        }
    }
}
