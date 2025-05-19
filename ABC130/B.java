/*
*足してそれを出力
*
*
*/

import java.util.*;

public class Main{
  public static void main(String[] args){
    Scanner sc = new Scanner(System.in);
    int num = sc.nextInt();
    int ll = sc.nextInt();
    int x = 0;
    int count = 1;
    
    for(int i = 0 ; i < num ; i++){
      int curx = sc.nextInt();
      x += curx;
      if(x <= ll){
        count++;
      }
    }
    System.out.println(count);
  }
}  
