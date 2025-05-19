/*
*P1~Pnまで　降順に並び替えて　和の公式を使うと求まる
*
*/

import java.util.*;
public class Main{
  public static void main(String[] args){
    Scanner sc = new Scanner(System.in);
    long n = sc.nextLong()-1;
    long sum =0;
    
    sum = n*(n+1)/2;
    
    System.out.println(sum);
  }
}
