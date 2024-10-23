/*
*Atcoder  ABC220 Base K
* 基数変換(n進法)
*/

import java.util.*;

public class Main{
  public static void main(String[] args){
    Scanner sc = new Scanner(System.in);
    int baseNumber = sc.nextInt();  //進数
    long a = sc.nextLong();
    long b = sc.nextLong();
    long a10 = 0;                   //aを10進数変換した値
    long b10 = 0;                   //bを10進数変換した値
    long exponent = 1;  //指数
    
   while(a != 0 || b != 0){
      if(a!= 0){
        long targetA = a%10;          //１の位から取り出していく
        a10 += targetA*exponent;
        a = a/10;
      }
      if(b!=0){
        long targetB = b%10;
        b10 += targetB*exponent;
        b = b/10;
      }
      exponent *= baseNumber;
    }
    System.out.println(a10*b10);
  }
