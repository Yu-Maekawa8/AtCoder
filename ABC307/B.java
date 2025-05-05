/*
*与えられた2つの文を組み合わせ回文は作れるかどうか
*
*/

import java.util.*;
import java.math.*;

public class Main {
    public static void main(String[] args) {
        try (Scanner sc = new Scanner(System.in)) {
            int n = sc.nextInt();
            String[] arr = new String[n];
            for (int i = 0; i < n; i++) {
                arr[i] = sc.next();
            }
            for(int i = 0 ; i < n ; i++){
                for (int j = 0; j < n; j++) {
                    if(i == j){
                        continue;
                    }
                    String tmp = arr[i]+arr[j];
                    for (int k = 0; k <tmp.length()/2 ; k++) {
                        if(tmp.charAt(k) != tmp.charAt(tmp.length()-1-k)){
                            break;
                        }else{
                            if(k == (tmp.length()/2) -1 ){
                                System.out.println("Yes");
                                return;
                            }
                        }
                    }
                }
            }
            System.out.println("No");
        }
    }
}
