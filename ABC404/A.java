import java.util.*;

public class Main {
    public static void main(String[] args) {
        try (Scanner sc = new Scanner(System.in)) {
            String s = sc.next();
            boolean[] b = new boolean[26];

            for(int i = 0 ; i < s.length(); i++){
                if(b[s.charAt(i) - 'a'] == false){
                    b[s.charAt(i) - 'a'] = true;
                }
            }
            for(int i = 0 ; i < b.length; i++){
                if(b[i] == false){
                    System.out.println((char)(i + 'a'));
                    return;
                }
            }
            
        }
    }
}
