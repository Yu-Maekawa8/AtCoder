/*
*if文分岐
*
*/

import java.util.*;
    public class Main{
      public static void main(String[] args){
        Scanner sc = new Scanner(System.in);
        int age = sc.nextInt();
        int price = sc.nextInt();
        
        if(age>=13){
            System.out.println(price);
        }else if(age >=6){
            System.out.println(price/2);
        }else{
            System.out.println(0);
        }
      }
    }
