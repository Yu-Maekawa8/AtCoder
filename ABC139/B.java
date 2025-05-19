/*
*差し込む分の一つを抜き足していく、カウント数越えたら出力
*
*
*/

import java.util.*;
public class Main{
  public static void main(String[] args){
    Scanner sc = new Scanner(System.in);
    int n = sc.nextInt();
    int ul = sc.nextInt();
    int pt = 1;
    int count =0;
    
    while(ul > pt){
      pt += (n-1);
      count++;
    }
    System.out.println(count);
  }
}
