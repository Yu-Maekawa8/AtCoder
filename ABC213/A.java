// AC済み問題: abc213_a
// 提出日時: 2024-11-01 09:17:15
// 実行時間: 76ms
// 注意: AtCoderは public class Main だが、IDE用に public class A に変更

package ABC213;

import java.util.*;
public class A{
  public static void main(String[] args){
    Scanner sc = new Scanner(System.in);
    int num1 = sc.nextInt();
    int num2 = sc.nextInt();
    int[] num12 = new int[8];
    int[] num22 = new int[8];
    int i =0;
    int answer = 0;
    int weight = 1;
    
    while(num1 != 0){
      num12[i] = num1%2;
      num1 /= 2;
      i++;
    }
    i = 0;
    while(num2 != 0){
      num22[i] = num2%2;
      num2 /= 2;
      i++;
    }
    for(int j = 0 ; j < 8 ; j++){
      if(num12[j] != num22[j]){
        answer += weight;
      }
      weight *= 2;
    }
    System.out.println(answer);
  }
}