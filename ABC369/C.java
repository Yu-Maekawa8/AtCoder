// AC済み問題: abc369_c
// 提出日時: 2024-11-22 18:01:46
// 実行時間: 485ms
// 注意: AtCoderは public class Main だが、IDE用に public class C に変更

package ABC369;

import java.util.*;

public class C {
    public static void main(String [] args) {
        try(Scanner sc = new Scanner(System.in)){
            int n = sc.nextInt();
            long ans = 0;
            long rev = 0;
            long[] s = new long[n];
            for(int i = 0 ; i < n ; i++){
                s[i] = sc.nextLong();
            }
            if(n != 1){
                long tmp = s[1]-s[0];
                long cnt = 1;
                for(int i = 0 ; i < n-1 ; i++){
                    if(tmp == s[i+1]-s[i] ){
                        cnt++;
                    }else{
                        ans += (cnt*(cnt+1)/2);
                        cnt = 1;
                        tmp = s[i+1]-s[i];
                        i--;
                        rev++;
                    }

                    if(i == n-2){
                        ans += (cnt*(cnt+1)/2);
                    }
                }
            }
            System.out.println(n == 1 ? 1: ans-rev);
        }
    }
}