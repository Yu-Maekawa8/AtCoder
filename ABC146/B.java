/*
*n個分アルファベットを進める
*
*/


import java.util.*;

public class Main {
    public static void main(String[] args) {
        try (Scanner sc = new Scanner(System.in)) {
            int n = sc.nextInt();
            char[] s = sc.next().toCharArray();

            for(int i = 0 ; i < n; i++){
                for(int j = 0 ; j < s.length ; j++){
                    if(s[j] == 'Z'){
                        s[j] = 'A';
                    }else{
                        s[j] = (char)(s[j] + 1);
                    }
                    
                }
            }
            System.out.println(s);
        }
    }
}
