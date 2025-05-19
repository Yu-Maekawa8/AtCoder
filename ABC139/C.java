/*
*ランレングス方式で加算する
*
*/


import java.util.*;
public class Main{
  public static void main(String[] args){
    Scanner sc = new Scanner(System.in);
    int n = sc.nextInt();
    long[] x = new long[n];
    long[] move = new long[n];
    int count = 0;
    int st = -1;
    
    for(int i = 0 ; i < n ; i++){
      x[i] = sc.nextLong();
    }
    
    for(int i = 0 ; i < n-1 ; i++){
      if(st == -1){
        st = 0;
      }
      if(x[i] >= x[i+1]){
        move[st]++;
      }else{
        st = i+1;
      }
    }
    
    Arrays.sort(move);
    
    System.out.println(move[move.length-1]);
  }
}
