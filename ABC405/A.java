

import java.util.*;
import java.math.*;

public class Main {
    public static void main(String[] args) {
        try (Scanner sc = new Scanner(System.in)) {
            int n = sc.nextInt();
            int x = sc.nextInt();

            if(x == 1){
                if(n >=1600 && n <= 2999){
                    System.out.println("Yes");
                    return;
                }else{
                    System.out.println("No");
                    return;
                }
            }else if(x == 2){
                if(n >= 1200 && n <= 2399){
                    System.out.println("Yes");
                    return;
                }else{
                    System.out.println("No");
                    return;
                }
            }
            System.out.println("No");
        }
    }
}
