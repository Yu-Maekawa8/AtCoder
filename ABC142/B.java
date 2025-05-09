/*
* n人いて、その中でkcm以上の人は何人？？
*
*
*/


import java.util.*;

public class Main {
    public static void main(String[] args) {
        try (Scanner sc = new Scanner(System.in)) {
            int n = sc.nextInt();
            int k = sc.nextInt();

            int cnt = 0;

            for(int i = 0 ; i < n ; i++){
                int tmp = sc.nextInt();
                if(k <= tmp){
                    cnt++;
                }
            }
            System.out.println(cnt);

        }
    }
}
