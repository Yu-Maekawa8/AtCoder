import java.util.*;

public class Main {
    public static void main(String [] args) {
        try(Scanner sc = new Scanner(System.in)){
            int n = sc.nextInt();
            int[] amb = new int[2*n+1];
            int[] era = new int[n];
            for(int i = 0 ; i < n ; i++){
                era[i] = sc.nextInt();
            }
            Arrays.fill(amb,-1);
            amb[0] = 0;

            for(int i = 0 ; i < n ; i++){
                amb[2*(i+1)-1]= amb[era[i]-1]+1 ;
                amb[2*(i+1)]= amb[era[i]-1]+1 ;
            }

            for(int i = 0 ; i < amb.length ; i++){
                System.out.println(amb[i]);
            }
        }
    }
}