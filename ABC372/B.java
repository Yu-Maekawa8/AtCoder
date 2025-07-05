// AC済み問題: abc372_b
// 提出日時: 2024-10-21 16:57:10
// 実行時間: 85ms
// 注意: AtCoderは public class Main だが、IDE用に public class B に変更

package ABC372;

import java.util.*;
public class B{
    public static void main(String [] args){
        Scanner sc = new Scanner(System.in);
        int target = sc.nextInt();
        int remainder = target;
        int sum = 0;
        int count = 0;
        int i= 10;
        int j = 0;
        int[] number = new int[20]; 
        for(; i>=0 ; i--){
          if((int)Math.pow(3,i) <= target){
            break;
          }
        }
        while(remainder != 0){
          if((int)Math.pow(3,i) <= remainder){
            remainder -= (int)Math.pow(3,i);
            count++;
            number[j] = i;
            j++;
          }else{
            i--;
          }
        }
        System.out.println(count);
        
        for(int k = 0 ; k < count ; k++){
          System.out.print(number[k]+" ");
        }
    }
}