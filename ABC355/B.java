import java.util.*;
import java.math.*;

public class Main {
    public static void main(String[] args) {
        try (Scanner sc = new Scanner(System.in)) {
            int[] ar = new int[sc.nextInt()];
            int[] ar2 = new int[sc.nextInt()];
            Arrays.sort(ar);
            Arrays.sort(ar2);
            for (int i = 0; i < ar.length; i++) {
                ar[i] = sc.nextInt();
            }
            for (int i = 0; i < ar2.length; i++) {
                ar2[i] = sc.nextInt();
            }
            int[] ans = new int[ar.length + ar2.length];
            int cnt1 = 0, cnt2 = 0;
            int jd = -1;
            for (int i = 0; i < ans.length; i++) {
                if(cnt1 == ar.length || cnt2 == ar2.length) {
                    break;
                }
                if(ar[cnt1] < ar2[cnt2]) {
                    ans[i] = ar[cnt1++];
                    if(jd == 1) {
                        System.out.println(3);
                        System.out.println("Yes");
                        return;
                    }
                    jd = 1;
                } else {
                    ans[i] = ar2[cnt2++];
                    if(jd == 2) {
                        System.out.println(1);
                        System.out.println("Yes");
                        return;
                    }
                    jd = 2;
                }
            }
            if(ar.length - cnt1 >=2 || ar2.length - cnt2 >= 2){
                System.out.println(2);
                System.out.println("Yes");
            }else{
                System.out.println("No");
            }
            
        }
    }
}
