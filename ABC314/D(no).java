import java.util.*;
import java.math.*;

            // List で　kind分作るかもそれから　rotateするかも

public class Main {
    public static void main(String[] args) {
        try (Scanner sc = new Scanner(System.in)) {
            int n = sc.nextInt();
            String s = sc.next();
            int q = sc.nextInt();

            StringBuilder sb = new StringBuilder();

            for(int i = 0 ; i < q ; i++){
                int op = sc.nextInt();
                int idx = sc.nextInt() - 1;
                char c = sc.next().charAt(0);
                
                if(op == 1){
                    String newSt = s.substring(0,idx) + c + s.substring(idx + 1, n);
                    s = newSt;
                }else if(op == 2){
                    s = s.toLowerCase();
                }else if(op == 3){
                    s = s.toUpperCase();
                }
            }
            System.out.println(s);
        }
    }
}
