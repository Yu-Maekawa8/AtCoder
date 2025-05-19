/*
* 一致してたらカウント
*
*/

import java.util.*;
public class Main{
  public static void main(String[] args){
    Scanner sc = new Scanner(System.in);
    String[] s1 = sc.nextLine().split("");
    String[] s2 = sc.nextLine().split("");
    int count = 0;
    
    for(int i = 0 ; i < 3 ; i++){
      if(s1[i].equals(s2[i])){
        count++;
      }
    }
    System.out.println(count);
  }
}
