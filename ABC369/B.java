// AC済み問題: abc369_b
// 提出日時: 2024-11-22 20:15:55
// 実行時間: 94ms
// 注意: AtCoderは public class Main だが、IDE用に public class B に変更

package ABC369;

import java.util.*;

public class B {
    public static void main(String [] args) {
        try(Scanner sc = new Scanner(System.in)){
            int ans = 0;
            int n  = sc.nextInt();
            int[]dis = new int[n];
            String[] hd = new String[n];
            for(int i = 0 ; i < n ; i++){
                dis[i] = sc.nextInt();
                hd[i] = sc.next();
                sc.nextLine();
            }
            int l = 0;
            int r = 0;
            for(int i = 0 ; i < n ; i++){
                if(hd[i].equals("L")){
                    if(l !=0){
                        ans += Math.abs(l-dis[i]) ;
                    }
                    l = dis[i];
                }else{
                    if(r !=0){
                        ans += Math.abs(r-dis[i]) ;
                    }
                    r = dis[i];
                }
            }


            System.out.println(ans);
        }
    }
}