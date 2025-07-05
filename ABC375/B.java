// AC済み問題: abc375_b
// 提出日時: 2024-10-20 14:23:29
// 実行時間: 541ms
// 注意: AtCoderは public class Main だが、IDE用に public class B に変更

package ABC375;

import java.util.*;
public class B{
    public static void main(String [] args){
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();        //点の数
        int cx = 0;                  //初期位置x
        int cy = 0;                  //初期位置y
        int nx = 0;                  //次のx
        int ny = 0;                  //次のy
        double distance = 0.0;
        
        for(int i = 1 ; i <= n ; i++){
            nx = sc.nextInt();                     //次に移動するx座標
            ny = sc.nextInt();                     //次に移動するy座標
            
            distance += Math.sqrt(Math.pow(nx - cx, 2) + Math.pow(ny - cy, 2)); //距離計算
            
            cx = nx;
            cy = ny;
        }
        distance += Math.sqrt(Math.pow(0 - cx, 2) + Math.pow(0 - cy, 2)); //距離計算(最後は原点にも戻る)
        System.out.printf("%.20f\n",distance);
    }
}