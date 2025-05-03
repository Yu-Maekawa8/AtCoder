
/**
 * 5の倍数に切り上げる方法
 */


import java.util.*;

public class Main {
    public static void main(String[] args) {
        try (Scanner sc = new Scanner(System.in)) {
            int n = sc.nextInt();
            int ans = 0;

            ans = (n+2)/5 *5;
            if(ans >100){
                ans = 100;
            }

            System.out.println(ans);
        }
    }
}
