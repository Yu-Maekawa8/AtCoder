import java.util.*;

public class Main {
    public static void main(String [] args) {
        try(Scanner sc = new Scanner(System.in)){
            int n =sc.nextInt();
            int x = sc.nextInt();
            int ans = 0;
            int[] ar = new int[n];
            for(int i = 0 ; i < n ; i++){
                ar[i] = sc.nextInt();
            }
            for(int i = 0 ;i < n; i++){
                if(ar[i] == x){
                    ans = i;
                    break;
                }
            }
            System.out.println(ans+1);

        }
    }
    public static void swap(Object[] a ,int i ,int j) {
        Object tmp = a[i];
        a[i] = a[j];
        a[j] = tmp;
        }
}