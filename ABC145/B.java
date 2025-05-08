/*
*与えられた文字列Sが　S=T+Tとなる　文字列Tが存在するかどうか
*
*/


import java.util.*;

public class Main {
    public static void main(String[] args) {
        try (Scanner sc = new Scanner(System.in)) {
            int n = sc.nextInt();
            String s = sc.next();
            
            if(n%2 != 0) {
                System.out.println("No");
                return;
            }
            for (int i = 0; i < s.length()/2; i++) {
                if(s.charAt(i) != s.charAt(s.length()/2 + i)) {
                    System.out.println("No");
                    return;
                }
            }
            
            System.out.println("Yes");
        }
    }
}
